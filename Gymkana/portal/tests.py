import datetime
import pytz
import json
import shutil

from .models import New, Event

from django.test import TestCase
from django.test.client import MULTIPART_CONTENT, Client
from django.shortcuts import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

TEST_DIR = 'test_data'

class index_tests(TestCase):

    def setUp(self):
        New.objects.create(title="Título 1", subtitle="Subtítulo 1", body="Cuerpo 1")
        New.objects.create(title="Título 2", subtitle="Subtítulo 2", body="Cuerpo 2")
        New.objects.create(title="Título 3", subtitle="Subtítulo 3", body="Cuerpo 3")

        Event.objects.create(title="Título 1", subtitle="Subtítulo 1", body="Cuerpo 1", start_date=datetime.datetime(2021, 9, 14, 8, 17, 0, 0, tzinfo=pytz.UTC), end_date=datetime.datetime(2021, 9, 17, 0, 0, 0, 0, tzinfo=pytz.UTC))
        Event.objects.create(title="Título 2", subtitle="Subtítulo 2", body="Cuerpo 2", start_date=datetime.datetime(2021, 9, 25, 9, 0, 0, 0, tzinfo=pytz.UTC), end_date=datetime.datetime(2021, 9, 27, 0, 0, 0, 0, tzinfo=pytz.UTC))
        Event.objects.create(title="Título 3", subtitle="Subtítulo 3", body="Cuerpo 3", start_date=datetime.datetime(2021, 10, 1, 18, 0, 0, 0, tzinfo=pytz.UTC), end_date=datetime.datetime(2021, 10, 3, 0, 0, 0, 0, tzinfo=pytz.UTC))

        self.client = Client()

    def test_home_page(self):
        url = reverse('portal:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal/index.html')

    def test_create_news(self):
        self.assertQuerysetEqual(New.objects.filter(title='Título 1'), ['<New: New object (1)>'])
        self.assertQuerysetEqual(New.objects.filter(title='Título 2'), ['<New: New object (2)>'])
        self.assertQuerysetEqual(New.objects.filter(title='Título 3'), ['<New: New object (3)>'])

    def test_create_events(self):
        self.assertQuerysetEqual(Event.objects.filter(title='Título 1'), ['<Event: Event object (1)>'])
        self.assertQuerysetEqual(Event.objects.filter(title='Título 2'), ['<Event: Event object (2)>'])
        self.assertQuerysetEqual(Event.objects.filter(title='Título 3'), ['<Event: Event object (3)>'])

"""
Tests for NEWS with FBV
"""

class new_creation_tests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_creation_new_page(self):
        url = reverse('portal:new_form')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal/new_form.html')

    def test_create_new(self):
        url = reverse('portal:new_form')
        new_content = {'title':'Título 4', 'subtitle':'Test #5', 'body':'Esta es una noticia de prueba.'}
        response = self.client.post(url, new_content)
        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(New.objects.filter(title='Título 4'), ['<New: New object (1)>'])

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_create_new_image(self):
        news_before = New.objects.count()
        url = reverse('portal:new_form')
        image_path = 'media/default.jpg'
        image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        new_content = {'title':'Título 5', 'subtitle':'Test #6', 'body':'Esta es una noticia de prueba.', 'image':image}
        response = self.client.post(url, new_content, content_type=MULTIPART_CONTENT)
        news_after = New.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertGreater(news_after, news_before)

    def test_create_new_image_error(self):
        news_before = New.objects.count()
        url = reverse('portal:new_form')
        image_path = 'media/default.jpg'
        image = SimpleUploadedFile(name='test_image.gif', content=open(image_path, 'rb').read(), content_type='image/gif')
        new_content = {'title':'Título 5', 'subtitle':'Test #6', 'body':'Esta es una noticia de prueba.', 'image':image}
        response = self.client.post(url, new_content, content_type=MULTIPART_CONTENT)
        news_after = New.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(news_after, news_before)

     

class new_read_tests(TestCase):

    def setUp(self):
        self.client = Client()
        New.objects.create(title="Título 5", subtitle="Subtítulo 5", body="Cuerpo 5")

    def test_404_read_new(self):
        url = reverse('portal:read_new', kwargs={'new_id': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_read_new(self):
        url = reverse('portal:read_new', kwargs={'new_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(New.objects.filter(title='Título 5'), ['<New: New object (1)>'])
        self.assertTemplateUsed(response, 'portal/read_new.html')


class new_edit_tests(TestCase):

    def setUp(self):
        self.client = Client()
        self.new_1 = New.objects.create(title="Título 6", subtitle="Subtítulo 6", body="Cuerpo 6")

    def test_404_edit_test(self):
        url = reverse('portal:edit_new', kwargs={'new_id':2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_edit_new_page(self):
        url = reverse('portal:edit_new', kwargs={'new_id':1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'portal/edit_new.html')
        self.assertEqual(response.status_code, 200)


    def test_edit_new(self):
        url = reverse('portal:edit_new', kwargs={'new_id':1})
        edit_content = {'title':'Título editado', 'subtitle':'Subtítulo editado', 'body':'Cuerpo editado'}
        response = self.client.post(url, edit_content)
        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(New.objects.filter(title='Título editado'), ['<New: New object (1)>'])

class new_delete_test(TestCase):

    def setUp(self):
        self.client = Client()
        self.new_1 = New.objects.create(title="Título 7", subtitle="Subtítulo 7", body="Cuerpo 8")

    def test_404_delete(self):
        url = reverse('portal:delete_new', kwargs={'new_id':2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_new_page(self):
        url = reverse('portal:delete_new', kwargs={'new_id':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal/delete_form.html')
        self.assertQuerysetEqual(New.objects.filter(title='Título 7'), ['<New: New object (1)>'])

    def test_delete_new(self):
        url = reverse('portal:delete_new', kwargs={'new_id':1})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(New.objects.filter(title='Título 7'), [])

"""
Tests for NEWS with CBV
"""

class new_creation_tests_class(TestCase):

    def setUp(self):
        self.client = Client()

    def test_creation_new_page(self):
        url = reverse('portal:new_form_class')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal/new_form.html')

    def test_create_new(self):
        url = reverse('portal:new_form_class')
        new_content = {'title':'Título 4', 'subtitle':'Test #5', 'body':'Esta es una noticia de prueba.'}
        response = self.client.post(url, new_content)
        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(New.objects.filter(title='Título 4'), ['<New: New object (1)>'])

class new_read_tests_class(TestCase):

    def setUp(self):
        self.client = Client()
        New.objects.create(title="Título 5", subtitle="Subtítulo 5", body="Cuerpo 5")

    def test_404_read_new(self):
        url = reverse('portal:read_new_class', kwargs={'pk': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_read_new(self):
        url = reverse('portal:read_new_class', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(New.objects.filter(title='Título 5'), ['<New: New object (1)>'])
        self.assertTemplateUsed(response, 'portal/read_new.html')

class new_edit_tests_class(TestCase):

    def setUp(self):
        self.client = Client()
        self.new_1 = New.objects.create(title="Título 6", subtitle="Subtítulo 6", body="Cuerpo 6")

    def test_404_edit_test(self):
        url = reverse('portal:edit_new_class', kwargs={'pk':2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_edit_new_page(self):
        url = reverse('portal:edit_new_class', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'portal/edit_new.html')
        self.assertEqual(response.status_code, 200)

    def test_edit_new(self):
        url = reverse('portal:edit_new_class', kwargs={'pk':1})
        edit_content = {'title':'Título editado', 'subtitle':'Subtítulo editado', 'body':'Cuerpo editado'}
        response = self.client.post(url, edit_content)
        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(New.objects.filter(title='Título editado'), ['<New: New object (1)>'])

class new_delete_test_class(TestCase):

    def setUp(self):
        self.client = Client()
        self.new_1 = New.objects.create(title="Título 7", subtitle="Subtítulo 7", body="Cuerpo 8")

    def test_404_delete(self):
        url = reverse('portal:delete_new_class', kwargs={'pk':2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_new_page(self):
        url = reverse('portal:delete_new_class', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal/delete_form.html')
        self.assertQuerysetEqual(New.objects.filter(title='Título 7'), ['<New: New object (1)>'])

    def test_delete_new(self):
        url = reverse('portal:delete_new_class', kwargs={'pk':1})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(New.objects.filter(title='Título 7'), [])

"""
Tests for events
"""

class event_creation_tests_class(TestCase):

    def setUp(self):
        self.client = Client()

    def test_creation_event_page(self):
        url = reverse('portal:event_form_class')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal/event_form.html')

    def test_create_event(self):
        url = reverse('portal:event_form_class')
        event_content = {'title':'Título 1', 'subtitle':'Test', 'body':'Evento de preuba.', 'start_date':'20/10/2021', 'end_date':'21/10/2021'}
        response = self.client.post(url, event_content)
        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(Event.objects.filter(title='Título 1'), ['<Event: Event object (1)>'])

class event_read_tests_class(TestCase):

    def setUp(self):
        self.client = Client()
        Event.objects.create(title="Título 4", subtitle="Subtítulo 4", body="Cuerpo 4", start_date=datetime.datetime(2021, 9, 14, 8, 17, 0, 0, tzinfo=pytz.UTC), end_date=datetime.datetime(2021, 9, 17, 0, 0, 0, 0, tzinfo=pytz.UTC))

    def test_404_read_event(self):
        url = reverse('portal:read_event_class', kwargs={'pk': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_read_new(self):
        url = reverse('portal:read_event_class', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(Event.objects.filter(title='Título 4'), ['<Event: Event object (1)>'])
        self.assertTemplateUsed(response, 'portal/read_event.html')

class event_edit_tests_class(TestCase):

    def setUp(self):
        self.client = Client()
        self.event_1 = Event.objects.create(title="Título 5", subtitle="Subtítulo 5", body="Cuerpo 5", start_date=datetime.datetime(2021, 9, 14, 8, 17, 0, 0, tzinfo=pytz.UTC), end_date=datetime.datetime(2021, 9, 17, 0, 0, 0, 0, tzinfo=pytz.UTC))

    def test_404_edit_test(self):
        url = reverse('portal:edit_event_class', kwargs={'pk':2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_edit_event_page(self):
        url = reverse('portal:edit_event_class', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'portal/edit_event.html')
        self.assertEqual(response.status_code, 200)

    def test_edit_event(self):
        url = reverse('portal:edit_event_class', kwargs={'pk':1})
        edit_content = {'title':'Título editado', 'subtitle':'Subtítulo editado', 'body':'Cuerpo editado', 'start_date':'20/10/2021', 'end_date':'21/10/2021'}
        response = self.client.post(url, edit_content)
        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(Event.objects.filter(title='Título editado'), ['<Event: Event object (1)>'])

class event_delete_test_class(TestCase):

    def setUp(self):
        self.client = Client()
        self.event_1 = Event.objects.create(title="Título 6", subtitle="Subtítulo 6", body="Cuerpo 6", start_date=datetime.datetime(2021, 9, 14, 8, 17, 0, 0, tzinfo=pytz.UTC), end_date=datetime.datetime(2021, 9, 17, 0, 0, 0, 0, tzinfo=pytz.UTC))

    def test_404_delete(self):
        url = reverse('portal:delete_event_class', kwargs={'pk':2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_event(self):
        url = reverse('portal:delete_event_class', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(Event.objects.filter(title='Título 6'), [])

class event_create_API(TestCase):

    def setUp(self):
        self.client = Client()

    def test_create_event_API(self):
        url = reverse('portal:create_event_api')
        event_content = {'title':'Título 1', 'subtitle':'Test', 'body':'Evento de preuba.', 'start_date':'2021-10-20T09:00', 'end_date':'2021-10-21T09:00'}
        response = self.client.post(url, event_content)
        self.assertEqual(response.status_code, 201)
        self.assertQuerysetEqual(Event.objects.filter(title='Título 1'), ['<Event: Event object (1)>'])

    def test_date_create_error(self):
        url = reverse('portal:create_event_api')
        event_content = {'title':'Título 2', 'subtitle':'Test', 'body':'Evento de preuba.', 'start_date':'2021-10-22T09:00', 'end_date':'2021-10-21T09:00'}
        response = self.client.post(url, event_content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'{"non_field_errors":["La fecha de comienzo no puede ser posterior a la fin"]}')
        self.assertQuerysetEqual(Event.objects.filter(title='Título 2'), [])

class event_read_API(TestCase):

    def setUp(self):
        self.client = Client()
        self.event_1 = Event.objects.create(title="Título 7", subtitle="Subtítulo 7", body="Cuerpo 7", start_date=datetime.datetime(2021, 9, 14, 8, 17, 0, 0, tzinfo=pytz.UTC), end_date=datetime.datetime(2021, 9, 17, 0, 0, 0, 0, tzinfo=pytz.UTC))

    def test_read_event_API(self):
        url = reverse('portal:event_detail_api',kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(Event.objects.filter(title='Título 7'), ['<Event: Event object (1)>'])

    def test_read_event_error_API(self):
        url = reverse('portal:event_detail_api',kwargs={'pk':2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'{"detail":"No encontrado."}')

class event_edit_API(TestCase):

    def setUp(self):
        self.client = Client()
        self.event_1 = Event.objects.create(title="Título 8", subtitle="Subtítulo 8", body="Cuerpo 8", start_date=datetime.datetime(2021, 9, 14, 8, 17, 0, 0, tzinfo=pytz.UTC), end_date=datetime.datetime(2021, 9, 17, 0, 0, 0, 0, tzinfo=pytz.UTC))


    def test_create_event_API(self):
        url = reverse('portal:event_detail_api', kwargs={'pk':1})
        event_content = json.dumps({'id':1,'title':'Título editado', 'subtitle':'Test', 'body':'Evento de preuba.', 'start_date':'2021-10-20T09:00', 'end_date':'2021-10-21T09:00'})
        response = self.client.put(url, event_content, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(Event.objects.filter(title='Título editado'), ['<Event: Event object (1)>'])

    def test_upadate_event_404_API(self):
        url = reverse('portal:event_detail_api', kwargs={'pk':2})
        event_content = json.dumps({'id':1,'title':'Título editado 2', 'subtitle':'Test', 'body':'Evento de preuba.', 'start_date':'2021-10-20T09:00', 'end_date':'2021-10-21T09:00'})
        response = self.client.put(url, event_content, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertQuerysetEqual(Event.objects.filter(title='Título editado 2'), [])

    def test_date_update_error_API(self):
        url = reverse('portal:event_detail_api', kwargs={'pk':1})
        event_content = json.dumps({'id':1,'title':'Título editado 2', 'subtitle':'Test', 'body':'Evento de preuba.', 'start_date':'2021-10-22T09:00', 'end_date':'2021-10-21T09:00'})
        response = self.client.put(url, event_content, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'{"non_field_errors":["La fecha de comienzo no puede ser posterior a la fin"]}')
        self.assertQuerysetEqual(Event.objects.filter(title='Título editado 2'), [])

class event_delete_API(TestCase):

    def setUp(self):
        self.client = Client()
        self.event_1 = Event.objects.create(title="Título 8", subtitle="Subtítulo 8", body="Cuerpo 8", start_date=datetime.datetime(2021, 9, 14, 8, 17, 0, 0, tzinfo=pytz.UTC), end_date=datetime.datetime(2021, 9, 17, 0, 0, 0, 0, tzinfo=pytz.UTC))

    def test_upadate_event_404_API(self):
        url = reverse('portal:event_detail_api', kwargs={'pk':2})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_event_API(self):
        url = reverse('portal:event_detail_api', kwargs={'pk':1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertQuerysetEqual(Event.objects.filter(title='Título 8'), [])
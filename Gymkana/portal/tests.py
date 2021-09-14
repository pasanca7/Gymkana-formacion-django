import datetime
from django.http import response
import pytz

from .models import New, Event
from .forms import  NewForm

from django.test import TestCase
from django.test.client import Client
from django.shortcuts import reverse



class index_tests(TestCase):

    def setUp(self):
        n1 = New.objects.create(title="Título 1", subtitle="Subtítulo 1", body="Cuerpo 1")
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




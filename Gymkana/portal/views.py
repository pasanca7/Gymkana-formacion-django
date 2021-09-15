import io

from django.urls.base import reverse_lazy

from portal.forms import NewForm, EventForm
from portal.models import Event, New
from django.utils import timezone
from django.views import generic
from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import HttpResponseRedirect
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from portal import serializers

class IndexView(generic.ListView):
    """
    Main view of the proyect
    """
    template_name = 'portal/index.html'
    context_object_name = 'lastest_news_list'


    def get_queryset(self):
        """
    We just want to see our last three news as 'lastest_news_list'
    """
        return New.objects.filter(publish_date__lte = timezone.now()).order_by('-publish_date')[:3]

    def get_context_data(self, **kwargs):
        """
        We just want to see our next three news as 'next_events_list'
        """
        context = super().get_context_data(**kwargs)
        context['next_events_list'] = Event.objects.filter(end_date__gte = timezone.now()).order_by('-end_date')[:3]
        return context

"""
Creation of new in FBV
"""
def create_new(request):
    if request.method == 'POST':
        new_form = NewForm(request.POST, request.FILES)        
        if new_form.is_valid():
            new_form.save()
            return redirect('portal:index')

    else:
        new_form = NewForm()
    return render(request, 'portal/new_form.html', {'form':new_form})

"""
Read new in FBV
"""
def read_new(request, new_id):
    new = get_object_or_404(New, pk = new_id)
    return render(request, 'portal/read_new.html', {'new': new})

"""
Edit new in FBV
"""
def edit_new(request, new_id):
    new = get_object_or_404(New, pk = new_id)
    if request.method == 'POST':
        form = NewForm(request.POST or None, files =  request.FILES or None, instance = new)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('portal:read_new',  args=[new_id]))
    else:
        form = NewForm(instance = new, initial={'new_id': new_id})
    return render(request, 'portal/edit_new.html', {'form':form})

"""
Delte new FBV
"""
def delete_new(request, new_id):
    new = get_object_or_404(New, pk = new_id)
    if request.method == 'POST':
        new.delete()
        return HttpResponseRedirect(reverse('portal:index'))
    else:
        return render(request, 'portal/delete_form.html', {'new':new})

"""
Creation of new CBV
"""
class create_new_class(generic.CreateView):
    template_name = 'portal/new_form.html'
    form_class = NewForm
    success_url = '/'

"""
Read new with CBV
"""
class read_new_class(generic.DetailView):
    model = New
    template_name = 'portal/read_new.html'
    
"""
Creation of new CBV
"""
class edit_new_class(generic.UpdateView):
    model = New
    template_name = 'portal/edit_new.html'
    form_class = NewForm

    def get_success_url(self):
        return reverse('portal:read_new_class', kwargs = {'pk':self.object.id})

"""
Delete new with CBV
"""
class delete_new_class(generic.DeleteView):
    model = New
    success_url = '/'
    template_name = 'portal/delete_form.html'

"""
Create events with CBV
"""
class create_event_class(generic.CreateView):
    template_name = 'portal/event_form.html'
    form_class = EventForm
    success_url = '/'

"""
Read events with CBV
"""
class read_event_class(generic.DeleteView):
    model = Event
    template_name = 'portal/read_event.html'

"""
Edit events with CBV
"""
class edit_event_class(generic.UpdateView):
    model = Event
    template_name = 'portal/edit_event.html'
    form_class = EventForm

    def get_success_url(self):
        return reverse('portal:read_event_class', kwargs = {'pk':self.object.id})

"""
Delete events with CBV and a Modal window
"""
class delete_event_class(generic.DeleteView):
    model = Event
    success_url = '/'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

"""
API methods for Events
"""
class EventApiView(APIView):

    serializer_class = serializers.event_serializer

    """
    Create an Event
    """
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

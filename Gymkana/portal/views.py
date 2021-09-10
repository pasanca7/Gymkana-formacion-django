import os
import io

from django.forms.utils import ErrorList

from portal.forms import NewForm
from portal.models import Event, New
from django.utils import timezone
from django.views import generic
from django.shortcuts import redirect, render
from PIL import Image

def image_to_byte_array(image:Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

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
def createNew(request):
    if request.method == 'POST':
        new_form = NewForm(request.POST, request.FILES)        
        if new_form.is_valid():
            new_form.save()
            return redirect('/portal/')
    else:
        new_form = NewForm()
    return render(request, 'portal/new_form.html', {'new_form':new_form})

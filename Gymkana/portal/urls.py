from django.urls import path

from . import views

app_name = 'portal'
urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index.html'),
    path('v1/news/create', views.createNew, name = 'new_form')
    ]
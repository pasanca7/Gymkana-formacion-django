from django.urls import path

from . import views

app_name = 'portal'
urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
    path('v1/news/create', views.create_new, name = 'new_form'),
    path('v1/news/<int:new_id>', views.read_new, name = 'read_new'),
    path('v1/news/<int:new_id>/edit', views.edit_new, name = 'edit_new'),
    path('v1/news/<int:new_id>/delete', views.delete_new, name = 'delete_new'),
    path('v2/news/create', views.create_new_class.as_view(), name = 'new_form_class'),
    path('v2/news/<int:pk>', views.read_new_class.as_view(), name = 'read_new_class'),
    ]
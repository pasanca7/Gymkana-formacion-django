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
    path('v2/news/<int:pk>/edit', views.edit_new_class.as_view(), name = 'edit_new_class'),
    path('v2/news/<int:pk>/delete', views.delete_new_class.as_view(), name = 'delete_new_class'),
    path('v2/events/create', views.create_event_class.as_view(), name = 'event_form_class'),
    path('v2/events/<int:pk>', views.read_event_class.as_view(), name = 'read_event_class'),
    path('v2/events/<int:pk>/edit', views.edit_event_class.as_view(), name = 'edit_event_class'),
    path('v2/events/<int:pk>/delete', views.delete_event_class.as_view(), name = 'delete_event_class'),
    path('api/events/', views.event_APIView_create.as_view(), name='create_event_api'),
    path('api/events/<int:pk>', views.event_APIView_detail.as_view(), name='event_detail_api'),
    ]
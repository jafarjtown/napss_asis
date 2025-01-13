from django.urls import path
from . import views


app_name = 'service'
urlpatterns = [
  path('', views.services, name='index'),
  path('new/', views.add_service, name='add'),
  path('details/<int:service_id>/', views.service_details, name='details'),
  path('cancel/<int:service_id>/', views.cancel_service, name='cancel'),
  path('complete/<int:service_id>/', views.complete_service, name='complete'),
  
  ]
# app/urls.py
from django.urls import path
from . import views


app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path("register_newsletter/", views.register_newsletter, name="register_newsletter"),

]

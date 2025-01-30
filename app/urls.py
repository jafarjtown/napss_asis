# app/urls.py
from django.urls import path
from . import views


app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('advance/search/', views.advance_search, name='advance_search'),
    path('about/', views.about, name='about'),
    path('representatives/', views.representatives, name='representatives'),
    path('contact/', views.contact, name='contact'),
    path("register_newsletter/", views.register_newsletter, name="register_newsletter"),

]

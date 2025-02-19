from django.urls import path
from . import views

app_name = 'reader'
urlpatterns = [
  path('', views.index, name='index'),
  path('new/', views.new, name='new'),
  path('edit/<int:content_id>/', views.edit, name='edit'),
  path('edit/title/<int:id>/', views.edit_title, name='edit-title'),
  path('snippets/', views.snippet, name='snippet'),
  path('update_book/<section_id>/<block>/', views.update_book, name='update_book'),
  ]
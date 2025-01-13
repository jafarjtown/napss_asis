from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
  path('', views.index, name='index'),
  path('read/<slug:slug>/', views.view_blog, name='read_blog'),
  path('comment/<int:page_id>/', views.comment_blog, name='comment'),
  path('admin/page/<slug:slug>/edit/', views.edit_blog, name='edit_blog'),
  path('admin/pages/', views.blog_list, name='blog_list'),
  path('admin/pages/new', views.add_blog, name='add_blog'),
  path('admin/media/', views.media_gallery, name='media'),
  path('admin/media/add/', views.add_media_gallery, name='add_media'),
  path('admin/media/update/<int:doc_id>/', views.update_media_gallery, name='update_media'),
  ]
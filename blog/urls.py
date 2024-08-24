from django.urls import path
from .views import blogs, read_blog, rate_blog, write_blog
app_name = "blog"
urlpatterns = [
  path('', blogs, name='blogs'),
  path('write/', write_blog, name='write'),
  path('read/<int:blog_id>/', read_blog, name='read_blog'),
  path('rate/<int:blog_id>/', rate_blog, name='rate_blog'),
  ]
  
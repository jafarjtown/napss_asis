
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.
class Document(models.Model):
  file = models.FileField(upload_to='documents')
  name = models.CharField(max_length=50)
  alt_text = models.CharField(max_length=50)
  

class Tag(models.Model):
  value = models.CharField(max_length=25)
  pass

class BloggerSite(models.Model):
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  pages = models.ManyToManyField('BlogPage', blank=True)
  documents = models.ManyToManyField('Document', blank=True)
  name = models.CharField(max_length=50)
  tags = models.ManyToManyField('Tag', blank=True)


class BlogPage(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=500)
  slug = models.CharField(max_length=500)
  summary = models.TextField()
  content = models.TextField()
  cover_image = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name='covers')
  gallery_images = models.ManyToManyField('Document', blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_on = models.DateTimeField(auto_now=True)
  
  next_page = models.OneToOneField('BlogPage', on_delete=models.SET_NULL, null=True, related_name='next', blank=True)
  previous_page = models.OneToOneField('BlogPage', on_delete=models.SET_NULL, null=True, related_name='previous', blank=True)
  
  
  childrens = models.ManyToManyField('BlogPage', blank=True, related_name='parents')
  tags = models.ManyToManyField('Tag', blank=True, related_name='blogs')
  
  allow_comment = models.BooleanField(default=False)
  is_publish = models.BooleanField(default=False)
  
  def save(self, *args, **kwargs):
    if self.slug == '':
      self.slug = slugify(self.title)
    return super(BlogPage, self).save(*args, **kwargs)
  
  def parent(self):
    if BlogPage.objects.filter(childrens__contains=self).exists():
      return BlogPage.objects.filter(childrens__contains=self)[0]
    return None
    
  def get_absolute_url(self):
    return reverse('blog:read_blog', kwargs={'slug':self.slug})

class BlogComment(models.Model):
  blog = models.ForeignKey(BlogPage, on_delete=models.CASCADE, related_name='comments')
  
  name = models.CharField(max_length=50)
  email = models.CharField(max_length=50)
  content = models.TextField()
  
  created_on = models.DateTimeField(auto_now_add=True)
  
  upvote = models.IntegerField(default=0)
  downvote = models.IntegerField(default=0)
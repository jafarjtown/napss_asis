from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class BlogPost(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=500)
  desc = models.TextField()
  content = models.TextField()
  cover = models.FileField(upload_to='blog cover', null=True)
  ratings = models.ManyToManyField('Rating', blank=True)
  publish = models.BooleanField(default=False)
  
  def user_rated(self, user__id):
    if user__id == None:
      return False
    users = [rating.user.id for rating in self.ratings.only('user__id')]
    return user__id in users

class Rating(models.Model):
  scale = models.PositiveIntegerField(default=0)
  comment = models.TextField()
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
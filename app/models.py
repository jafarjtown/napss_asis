from django.db import models

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    activate = models.BooleanField(default=True)

class Partner(models.Model):
  name = models.CharField(max_length=50)
  image = models.FileField(upload_to='partners')
  info = models.TextField()
  
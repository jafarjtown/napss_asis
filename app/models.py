from django.db import models

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    activate = models.BooleanField(default=True)

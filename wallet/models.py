from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Wallet(models.Model):
  account_number = models.CharField(max_length=10)
  owner = models.OneToOneField(User, on_delete=models.CASCADE)
  amount = models.IntegerField(default=1000)
  
  
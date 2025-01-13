from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ServicePriority(models.Model):
  name = models.CharField(max_length=35)
  level = models.IntegerField(default=0)
  information = models.TextField()

class ServiceType(models.Model):
  name = models.CharField(max_length=35)
  price = models.IntegerField(default=500)
  information = models.TextField()
  
class StudentService(models.Model):
  student = models.OneToOneField(User, on_delete=models.CASCADE)
  services = models.ManyToManyField('Service')
  
  def pending_services(self):
    return self.services.filter(completed=False)
    
class Service(models.Model):
  type = models.ForeignKey(ServiceType, on_delete=models.SET_NULL, null=True)
  priority = models.ForeignKey(ServicePriority, on_delete=models.SET_NULL, null=True)
  information = models.TextField()
  completed = models.BooleanField(default=False)
  accepted = models.BooleanField(default=False)
  price = models.IntegerField(default=0)
  
  def status(self):
    s = 'Pending'
    if self.completed:
      s = 'Completed'
    elif self.accepted:
      s = 'Processing'
    return s
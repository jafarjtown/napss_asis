from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
# Create your models here.


class Account(models.Model):
    GENDER = [
     ("M", "Male"),
     ("F", "Female"),
     ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")
    coins = models.PositiveIntegerField(default=0)
    department = models.ForeignKey('material.Department', on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER, default="M")
    date_of_birth = models.DateField(auto_now=False, default=timezone.now)
    profile_pic = models.FileField(upload_to='profile', null=True, blank=True, default="/media/imgs/default.png")
    
class FlaggedIssue(models.Model):
    response = models.TextField()
    email = models.CharField(max_length=50, default="")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    issued_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.tag

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

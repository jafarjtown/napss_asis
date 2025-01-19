from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
import uuid
# Create your models here.


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet', null=True, blank=True)
    nin = models.CharField(max_length=20)
    account_reference = models.CharField(max_length=100, unique=True)
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

class Beneficiary(models.Model):
  wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='beneficiaries')
  phone_number = models.CharField(max_length=255)

class LinkBeneficiary(models.Model):
  phone_number = models.CharField(max_length=255)

class GeneratedLink(models.Model):
  id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
  name = models.CharField(max_length=255)
  network = models.CharField(max_length=255)
  link_type = models.CharField(max_length=255)
  amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
  slot = models.IntegerField(default=3)
  available_slot = models.IntegerField(default=0)
  beneficiaries = models.ManyToManyField(LinkBeneficiary, blank=True)
  
  def display_amount(self):
    if self.link_type == 'data':
      return str(int(self.amount)) + 'MB'
    return '₦'+str(int(self.amount))
    
  def get_absolute_url(self):
    return reverse('wallet:generated_link', kwargs={'id':self.id})
    
  def progress(self):
    used_slot = self.slot - self.available_slot
    return used_slot / self.slot * 100
  
class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField()
    customer_name = models.CharField(max_length=255)
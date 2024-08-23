from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from app.models import FlaggedIssue, Request 
from .models import Account
import datetime


# @receiver(post_save, sender=User)  # Replace User with your model
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance, coins=5000)
    
        subject = "Welcome to Babuga's Library - Your School's Learning Hub!"
        email_content = render_to_string('welcome_mail.html', {'user_name': instance.get_full_name(), "admin": "Ja'afar Idris Tesla"})
        from_email = "Babuga's Library <support@babugas-library.com.ng>"
        recipient_list = [instance.email]
        
        send_mail = EmailMultiAlternatives(
        subject,
        '',  
        from_email,
        recipient_list,
        reply_to=["contacts@babugas-library.com.ng"]
    )
        send_mail.attach_alternative(email_content, "text/html")
        send_mail.send()

@receiver(post_save, sender=FlaggedIssue) 
def send_issue_email(sender, instance, created, **kwargs):
    if created:
        current_time = datetime.datetime.now()
        subject = "Course/Content Flag Received - Action Required"
        email_content = render_to_string('flag_mail.html', {'user_name': "User", "admin": "Ja'afar Idris Tesla", "reasons": instance.response, "date":current_time })
        from_email = "Babuga's Library <support@babugas-library.com.ng>"
        recipient_list = [instance.email]
        
        send_mail = EmailMultiAlternatives(
        subject,
        '',  
        from_email,
        recipient_list,
        reply_to=["contacts@babugas-library.com.ng"]
    )
        send_mail.attach_alternative(email_content, "text/html")
        send_mail.send()
        

@receiver(post_save, sender=Request) 
def send_request_email(sender, instance, created, **kwargs):
    if created:
        current_time = datetime.datetime.now()
        subject = "Thank You for Your Feedback and Requests"
        email_content = render_to_string('complain_mail.html', {'user_name': "User", "admin": "Ja'afar Idris Tesla", "request_type": instance.type, "description": instance.body, "topic": instance.topic, "date":current_time })
        from_email = "Babuga's Library <support@babugas-library.com.ng>"
        recipient_list = [instance.email]
        
        send_mail = EmailMultiAlternatives(
        subject,
        '',  
        from_email,
        recipient_list,
        reply_to=["contacts@babugas-library.com.ng"]
    )
        send_mail.attach_alternative(email_content, "text/html")
        send_mail.send()
        
        

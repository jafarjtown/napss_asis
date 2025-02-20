# myapp/management/commands/send_test_email.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Send a test email'

    def handle(self, *args, **kwargs):
        send_mail(
            'Test Subject',
            'Test message body.',
            'mail.abusitehub.com.ng',
            ['jafaridris82@gmail.com'],
            fail_silently=False,
        )
        self.stdout.write(self.style.SUCCESS('Test email sent!'))
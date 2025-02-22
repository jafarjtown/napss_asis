from django.shortcuts import render
from django.http import HttpResponse
from .mails import send_mail_users
from django.contrib.auth.models import User

def index(request):
    if request.htmx:
        if request.method == 'POST':
            print(request.POST)  # Debugging: Print POST data
            subject = request.POST.get('subject')
            to = request.POST.get('to')
            body = request.POST.get('body')
            attachment = None
            recipient = []
            
            # Handle file attachment
            if request.FILES:
                attachment = request.FILES.get('attachment')
            
            # Determine recipients
            if to == 'all':
                users = User.objects.all().only('email')
                recipient = [user.email for user in users]
            elif to == 'moderators':
                users = User.objects.filter(is_staff=True).only('email')
                recipient = [user.email for user in users]
            
            # Send email
            if recipient:  # Ensure there are recipients
                if attachment:
                    # Save the uploaded file temporarily
                    with open(f"/tmp/{attachment.name}", 'wb+') as destination:
                        for chunk in attachment.chunks():
                            destination.write(chunk)
                    # Send email with attachment
                    send_mail_users(subject, body, recipient, attachment_paths=[f"/tmp/{attachment.name}"])
                else:
                    # Send email without attachment
                    send_mail_users(subject, body, recipient)
            else:
                print("No recipients found.")
            
            return HttpResponse(status=204)  # HTMX expects a response
    return render(request, 'mail/index.html')

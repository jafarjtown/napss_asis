from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
  
def send_mail_users(subject, body, recipients, attachment_paths=None):
    email_content = render_to_string('mail.html', {'body': body, "admin": "Ja'afar Idris Tesla"})
    from_email = "Abusite Hub <noreply@abusitehub.com.ng>"
    recipient_list = recipients
    
    send_mail = EmailMultiAlternatives(
        subject,
        '',
        from_email,
        recipient_list,
        reply_to=["contact@abusitehub.com.ng"]
    )
    send_mail.attach_alternative(email_content, "text/html")
    
    if attachment_paths:
        for attachment_path in attachment_paths:
            try:
                with open(attachment_path, 'rb') as file:
                    file_name = attachment_path.split('/')[-1]
                    send_mail.attach(file_name, file.read(), 'application/octet-stream')
            except FileNotFoundError:
                print(f"File not found: {attachment_path}")
            except Exception as e:
                print(f"Error attaching file: {str(e)}")
    
    try:
        send_mail.send()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

from django.core.mail import EmailMessage


def send_email_notification(title, body, to, attachments=None):
    email = EmailMessage(title, body=body, to=to)
    email.content_subtype = 'html'
    if attachments:
        if isinstance(attachments, list):
            for m in attachments:
                email.attach(m['file_name'], m['file'], m['content_type'])
        else:
            email.attach(attachments['file_name'], attachments['file'], attachments['content_type'])
    email.send()


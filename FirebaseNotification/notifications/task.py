# task.py
from FirebaseNotification.celery import app
from django.core.mail import send_mail
from .models import Notification, Profile
from celery import shared_task
from FirebaseNotification import settings
from django.contrib.auth import get_user_model


@shared_task(bind=True)
def send_mail_func(self):
    users = get_user_model().objects.all()
    #timezone.localtime(users.date_time) + timedelta(days=2)
    for user in users:
        mail_subject = Notification.objects.filter(status='unread').last().title
        message = Notification.objects.filter(status='unread').last().body
        to_email = user.email
        send_mail(
            subject = mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
    return "Done"

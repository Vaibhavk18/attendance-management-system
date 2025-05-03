from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to Attendance Management System"
        message = f"Hi {instance.username},\n\nYour account has been created with role: {instance.role}."
        send_mail(subject, message, settings.EMAIL_HOST_USER, [instance.email])

from accounts.models import UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import send_welcome_email
from . models import UserProfile


@receiver(post_save, sender=UserProfile)
def user_added(sender, instance, created, **kwargs):
    if created:
        # Code to execute when a user is added through the admin panel
        user = UserProfile.objects.get(email=instance.email)
        user.set_password(f"{instance.name}@123")
        user.save()
        
        send_welcome_email(
            user=instance.name, email=instance.email, password=f"{instance.name}@123")

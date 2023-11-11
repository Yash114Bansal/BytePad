from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import UserProfile
from .utils import send_welcome_email
from .models import UserProfile


@receiver(post_save, sender=UserProfile)
def user_added(sender, instance, created, **kwargs):
    if created and not instance.is_staff:
        random_password = UserProfile.objects.make_random_password()

        user = UserProfile.objects.get(email=instance.email)
        user.set_password(random_password)
        user.save()

        send_welcome_email(
            user=instance.name, email=instance.email, password=random_password
        )

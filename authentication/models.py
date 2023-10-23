from django.utils import timezone
from django.db import models

class OTP(models.Model):
    mail = models.EmailField()
    otp = models.CharField(max_length=6)
    expiry_time = models.DateTimeField()

    def has_expired(self):
        return self.expiry_time < timezone.now()

    def __str__(self):
        return f"OTP for {self.mail}"

class AllowPasswordReset(models.Model):
    mail = models.EmailField()

    def __str__(self):
        return f"{self.mail}"
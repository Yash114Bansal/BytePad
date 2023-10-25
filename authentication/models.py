from django.utils import timezone
from django.db import models
from accounts.models import UserProfile

class OTP(models.Model):
    mail = models.EmailField()
    otp = models.CharField(max_length=6)
    expiry_time = models.DateTimeField()

    # Function To Check Validity of OTP
    def has_expired(self):
        return self.expiry_time < timezone.now()

    def __str__(self):
        return f"OTP for {self.mail}"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    expiry_time = models.DateTimeField()

    # Function To Check Validity of Password Reset Token
    def has_expired(self):
        return self.expiry_time < timezone.now()
    
    def __str__(self):
        return f"OTP for {self.user.first_name}"
from django.contrib import admin
from .models import OTP,PasswordResetToken

admin.site.register(OTP)
admin.site.register(PasswordResetToken)
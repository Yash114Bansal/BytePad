from django.contrib import admin
from .models import OTP,AllowPasswordReset

admin.site.register(OTP)
admin.site.register(AllowPasswordReset)
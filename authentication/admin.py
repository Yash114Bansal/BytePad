from django.contrib import admin
from .models import OTP,AllowPasswordReset
# Register your models here.

admin.site.register(OTP)
admin.site.register(AllowPasswordReset)
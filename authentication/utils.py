from django.core.mail import send_mail
from django.conf import settings
def send_otp(otp, email):
    subject = "Reset Password OTP"
    message = f"""
Dear User,

You've requested to reset your password for our application. Please use the following OTP to complete the process:

OTP: {otp}

If you didn't request this, please ignore this email. Your account's security is important to us.

Thank you for using our application!

Sincerely,
The BytePad Team
"""
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    return send_mail(subject, message, from_email, recipient_list)

from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(user,email, password):
    subject = "Welcome to BytePad!"
    message = f"""
Dear {user},

Welcome to BytePad, your one-stop destination for educational resources. We're excited to have you on board!

At BytePad, you can access a wide range of features, including:
- Previous year question papers and solutions
- Attendance tracking
- And much more!

We're committed to helping you achieve your educational goals. If you have any questions or need assistance, feel free to reach out to us anytime.


Sincerely,
The BytePad Team

Also, please make a note of your password for logging in: {password}
"""

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    return send_mail(subject, message, from_email, recipient_list)

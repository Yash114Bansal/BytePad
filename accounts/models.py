from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager

class UserProfile(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    email = models.EmailField(unique=True)
    is_department_head = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)

    objects = UserManager()

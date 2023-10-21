from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager
from .choices import *

class UserProfile(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    email = models.EmailField(unique=True)
    profile_picture = models.URLField()
    is_department_head = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    objects = UserManager()


class Course(models.Model):
    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=8, choices=BRANCH_CHOICES)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    course_code = models.CharField(max_length=6)

class StudentModel(models.Model):

    student_number = models.IntegerField(unique=True)
    roll_number = models.IntegerField(unique=True)
    current_semester = models.IntegerField(choices=SEMESTER_CHOICES)
    branch = models.CharField(max_length=8, choices=BRANCH_CHOICES)
    contact_number = models.IntegerField()
    date_of_birth = models.DateField()
    guardian_name = models.CharField(max_length=100)
    guardian_contact_number = models.IntegerField()
    courses = models.ManyToManyField(Course)

class FacultyModel(models.Model):

    employee_id = models.CharField(max_length=10, unique=True)
    contact_number = models.IntegerField()
    date_of_birth = models.DateField()
    courses = models.ManyToManyField(Course)
    department = models.CharField(max_length=8, choices=BRANCH_CHOICES)
    is_department_head = models.BooleanField(default=False)

    def __str__(self):
        return self.employee_id

from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager
from .choices import *


class UserProfile(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    username = None
    email = models.EmailField(unique=True,primary_key=True)
    name = models.CharField(max_length=200,null=True)

    profile_picture = models.ImageField(
        upload_to="profile_pics/", default="default.png"
    )

    is_department_head = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    objects = UserManager()


class Course(models.Model):
    name = models.CharField(max_length=100)
    #DATABASE 
    branch = models.CharField(max_length=8, choices=BRANCH_CHOICES)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    course_code = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.name} - {self.branch} - Semester{self.semester}"


class StudentModel(models.Model):

    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    roll_number = models.IntegerField(unique=True)
    current_semester = models.IntegerField(choices=SEMESTER_CHOICES)
    branch = models.CharField(max_length=8, choices=BRANCH_CHOICES)
    contact_number = models.BigIntegerField()
    date_of_birth = models.DateField()
    guardian_name = models.CharField(max_length=100)
    guardian_contact_number = models.BigIntegerField()

    def __str__(self):
        return str(self.roll_number)


class FacultyModel(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    contact_number = models.BigIntegerField()
    date_of_birth = models.DateField()
    courses = models.ManyToManyField(Course)
    department = models.CharField(max_length=8, choices=BRANCH_CHOICES)

    def __str__(self):
        return str(self.email)


class Batch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    year = models.IntegerField()
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    branch = models.CharField(max_length=8, choices=BRANCH_CHOICES)
    students = models.ManyToManyField(StudentModel)    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    
class BatchCourseFacultyAssignment(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    faculty = models.ForeignKey(FacultyModel, on_delete=models.CASCADE)
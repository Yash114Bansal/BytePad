from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager


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


class Branch(models.Model):
    name = models.CharField(max_length=8,primary_key=True)
    full_name = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name

class Semester(models.Model):
    name = models.CharField(max_length=10)
    semester = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=6,primary_key=True)

    def __str__(self):
        return f"{self.name} - {self.course_code}"


class StudentModel(models.Model):

    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    roll_number = models.IntegerField(unique=True)
    current_semester = models.ForeignKey(Semester,on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
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
    department = models.ForeignKey(Branch,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class Batch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    year = models.IntegerField()
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    students = models.ManyToManyField(StudentModel)    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    
class BatchCourseFacultyAssignment(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    faculty = models.ForeignKey(FacultyModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.batch} - {self.course} - {self.faculty}"
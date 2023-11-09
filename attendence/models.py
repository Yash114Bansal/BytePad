from django.db import models
from accounts.models import (
    Batch,
    Course,
    StudentModel
)
class Attendance(models.Model):
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)


class AttendanceSheet(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(unique=True)
    attendance_records = models.ManyToManyField(Attendance)

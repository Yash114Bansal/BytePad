from django.db import models
from accounts.models import (
    Batch,
    Course,
    StudentModel
)
class Attendance(models.Model):
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=(('present', 'Present'),
    ('absent', 'Absent'),))


class AttendanceSheet(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    attendance_records = models.ManyToManyField(Attendance)

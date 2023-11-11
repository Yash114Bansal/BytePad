from django.db import models
from accounts.models import (
    BatchCourseFacultyAssignment,
    StudentModel
)
class Attendance(models.Model):
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)
    def __str__(self) :
        return f"{self.student.user.name} - {self.date} - {self.present}"

class AttendanceSheet(models.Model):
    assignment = models.ForeignKey(BatchCourseFacultyAssignment, on_delete=models.CASCADE,null=True)
    date = models.DateField()
    attendance_records = models.ManyToManyField(Attendance)

    class Meta:
        unique_together = ('assignment', 'date')

    def __str__(self):
        return f"{self.assignment} - {self.date}"

from django.db import models
from accounts.models import BatchCourseFacultyAssignment, Batch

DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

class LectureNumberModel(models.Model):

    slot = models.IntegerField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"Lecture :{self.slot} ({self.start_time} :: {self.end_time})"

class LectureModel(models.Model):
    slot_number = models.ForeignKey(LectureNumberModel,on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)

    subject = models.ForeignKey(BatchCourseFacultyAssignment,on_delete=models.CASCADE)
    room = models.CharField(max_length=100)

    class Meta:
        unique_together = ("slot_number", "day","subject")
    
    def __str__(self):
        return f"Lecture of {self.subject.faculty.user.name} in {self.room} of {self.subject.course.name} slot: {self.slot_number.start_time}-{self.slot_number.end_time}"

class TimeTableModel(models.Model):
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE)
    lectures = models.ManyToManyField(LectureModel)

    def __str__(self):
        return f"{self.batch.name} - Timetable"
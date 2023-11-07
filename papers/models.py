from django.db import models
from accounts.models import Course

class SamplePaper(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/')
    year = models.IntegerField()
    semester = models.IntegerField()
    courses = models.ManyToManyField(Course)
    
    def __str__(self):
        return self.title
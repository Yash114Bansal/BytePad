from django.db import models
from accounts.models import Course,UserProfile
from django.core.validators import FileExtensionValidator

class SamplePaper(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'docx', 'txt', 'ppt', 'pptx', 'jpg', 'jpeg', 'png', 'gif'])
    ])

    year = models.IntegerField()
    semester = models.IntegerField()
    courses = models.ManyToManyField(Course)
    
    def __str__(self):
        return self.title

class SamplePaperSolution(models.Model):
    
    paper = models.ForeignKey(SamplePaper,on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'docx', 'txt', 'ppt', 'pptx', 'jpg', 'jpeg', 'png', 'gif'])
    ])

class MyCollections(models.Model):

    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    paper = models.ForeignKey(SamplePaper,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} : {self.paper.title}"

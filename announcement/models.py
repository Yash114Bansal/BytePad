from django.db import models
from django.core.validators import FileExtensionValidator
from accounts.models import Batch, UserProfile

allowed_formats = [
    "pdf",
    "doc",
    "docx",
    "txt",
    "ppt",
    "pptx",
    "jpg",
    "jpeg",
    "png",
    "gif",
]


class Announcement(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    document = models.FileField(
        upload_to="uploads/", validators=[FileExtensionValidator(allowed_formats)]
    )
    description = models.CharField(max_length=280)

    time = models.DateTimeField()
    venue = models.CharField(max_length=200)

    faculty_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class BatchSpecificAnnouncement(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    Batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    document = models.FileField(
        upload_to="uploads/", validators=[FileExtensionValidator(allowed_formats)]
    )
    description = models.CharField(max_length=280)

    time = models.DateTimeField()
    venue = models.CharField(max_length=200)

    def __str__(self):
        return self.title

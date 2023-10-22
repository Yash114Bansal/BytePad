from django.contrib import admin
from .models import Course,StudentModel,FacultyModel,UserProfile
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(StudentModel)
admin.site.register(FacultyModel)
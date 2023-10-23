from django.contrib import admin
from .models import Course, StudentModel, FacultyModel, UserProfile, Batch

# Register your models here.
admin.site.register(Course)
admin.site.register(Batch)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "is_department_head", "is_faculty", "is_student")


@admin.register(StudentModel)
class StudentModelAdmin(admin.ModelAdmin):
    list_display = ("id", "roll_number", "current_semester", "branch", "contact_number")


@admin.register(FacultyModel)
class FacultyModelAdmin(admin.ModelAdmin):
    list_display = ("id", "contact_number", "department", "is_department_head")

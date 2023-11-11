from django.contrib import admin
from .models import (
    Course,
    StudentModel,
    FacultyModel,
    UserProfile,
    Batch,
    BatchCourseFacultyAssignment,
    Semester,
    Branch,
)

admin.site.register(Course)
admin.site.register(Batch)
admin.site.register(BatchCourseFacultyAssignment)
admin.site.register(Semester)
admin.site.register(Branch)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("email", "is_department_head", "is_faculty", "is_student")
    fields = (
        "email",
        "name",
        "profile_picture",
        "is_department_head",
        "is_faculty",
        "is_student",
    )


@admin.register(StudentModel)
class StudentModelAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "roll_number",
        "current_semester",
        "branch",
        "contact_number",
    )


@admin.register(FacultyModel)
class FacultyModelAdmin(admin.ModelAdmin):
    list_display = ("user", "contact_number", "department")

from django.contrib import admin
from import_export.admin import ImportExportMixin
from import_export import resources
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

class BaseImportExportAdmin(ImportExportMixin, admin.ModelAdmin):
    pass

class UserProfileResource(resources.ModelResource):
    class Meta:
        model = UserProfile
        exclude = ('id', 'password', 'last_login', 'is_superuser', 'groups', 'user_permissions')
        import_id_fields=("email",)


class CourseResource(resources.ModelResource):
    class Meta:
        model = Course
        exclude = ("id",)
        import_id_fields=("course_code",)

class BranchResource(resources.ModelResource):
    class Meta:
        model = Branch
        exclude = ("id",)
        import_id_fields=("name",)

class SemesterResource(resources.ModelResource):
    class Meta:
        model = Semester
        exclude = ("id",)
        import_id_fields=("semester",)

@admin.register(Course)
class CourseAdmin(BaseImportExportAdmin):
    resource_class = CourseResource

@admin.register(Batch)
class BatchAdmin(BaseImportExportAdmin):
    pass

@admin.register(BatchCourseFacultyAssignment)
class BatchCourseFacultyAssignmentAdmin(BaseImportExportAdmin):
    pass

@admin.register(Semester)
class SemesterAdmin(BaseImportExportAdmin):
    pass

@admin.register(Branch)
class BranchAdmin(BaseImportExportAdmin):
    pass

@admin.register(UserProfile)
class UserProfileAdmin(BaseImportExportAdmin):
    list_display = ("email", "is_department_head", "is_faculty", "is_student")
    fields = (
        "email",
        "name",
        "profile_picture",
        "is_department_head",
        "is_faculty",
        "is_student",
    )
    resource_class = UserProfileResource

@admin.register(StudentModel)
class StudentModelAdmin(BaseImportExportAdmin):
    list_display = (
        "user",
        "roll_number",
        "current_semester",
        "branch",
        "contact_number",
    )

@admin.register(FacultyModel)
class FacultyModelAdmin(BaseImportExportAdmin):
    list_display = ("user", "contact_number", "department")

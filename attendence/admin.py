from django.contrib import admin
from accounts.admin import BaseImportExportAdmin
from .models import Attendance, AttendanceSheet

@admin.register(Attendance)
class AttendanceAdmin(BaseImportExportAdmin):
    pass

@admin.register(AttendanceSheet)
class AttendanceSheetAdmin(BaseImportExportAdmin):
    pass

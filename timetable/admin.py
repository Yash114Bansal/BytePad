from django.contrib import admin
from accounts.admin import BaseImportExportAdmin
from .models import LectureNumberModel, LectureModel, TimeTableModel

@admin.register(LectureNumberModel)
class AttendanceAdmin(BaseImportExportAdmin):
    pass

@admin.register(LectureModel)
class AttendanceSheetAdmin(BaseImportExportAdmin):
    pass

@admin.register(TimeTableModel)
class AttendanceSheetAdmin(BaseImportExportAdmin):
    pass

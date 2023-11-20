from django.contrib import admin
from accounts.admin import BaseImportExportAdmin
from .models import LectureNumberModel, LectureModel, TimeTableModel

@admin.register(LectureNumberModel)
class LectureNumberAdmin(BaseImportExportAdmin):
    pass

@admin.register(LectureModel)
class LectureAdmin(BaseImportExportAdmin):
    pass

@admin.register(TimeTableModel)
class TimeTableAdmin(BaseImportExportAdmin):
    pass

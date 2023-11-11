from django.contrib import admin
from accounts.admin import BaseImportExportAdmin
from .models import SamplePaper

@admin.register(SamplePaper)
class SamplePaperAdmin(BaseImportExportAdmin):
    pass

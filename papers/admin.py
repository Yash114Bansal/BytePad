from django.contrib import admin
from accounts.admin import BaseImportExportAdmin
from .models import SamplePaper,SamplePaperSolution

@admin.register(SamplePaper)
class SamplePaperAdmin(BaseImportExportAdmin):
    pass

@admin.register(SamplePaperSolution)
class SamplePaperSolutionAdmin(BaseImportExportAdmin):
    pass

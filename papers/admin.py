from django.contrib import admin
from accounts.admin import BaseImportExportAdmin
from .models import SamplePaper, SamplePaperSolution, MyCollections


@admin.register(SamplePaper)
class SamplePaperAdmin(BaseImportExportAdmin):
    pass

@admin.register(SamplePaperSolution)
class SamplePaperSolutionAdmin(BaseImportExportAdmin):
    pass

@admin.register(MyCollections)
class MyCollectionsAdmin(BaseImportExportAdmin):
    pass

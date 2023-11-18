from django.contrib import admin
from accounts.admin import BaseImportExportAdmin
from .models import Announcement, BatchSpecificAnnouncement


@admin.register(Announcement)
class AnnouncementAdmin(BaseImportExportAdmin):
    pass


@admin.register(BatchSpecificAnnouncement)
class BatchSpecificAnnouncementAdmin(BaseImportExportAdmin):
    pass

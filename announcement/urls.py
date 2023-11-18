from django.urls import path
from .views import (
    AnnouncementListView,
    AnnouncementCreateView,
    BatchSpecificAnnouncementCreateView,
    BatchSpecificAnnouncementListView,
)

urlpatterns = [
    path("create/", AnnouncementCreateView.as_view()),
    path("batch/create", BatchSpecificAnnouncementCreateView.as_view()),
    path("batch/", BatchSpecificAnnouncementListView.as_view()),
    path("", AnnouncementListView.as_view()),
]

from django.urls import path
from .views import AnnouncementListView,AnnouncementCreateView

urlpatterns = [
    path("create/",AnnouncementCreateView.as_view()),
    path("",AnnouncementListView.as_view()),
]

from django.urls import path
from .views import UserListCreateView, StudentDetailView, FacultyDetailView

urlpatterns = [
    path("users/", UserListCreateView.as_view(), name="user-list"),
    path("student/", StudentDetailView.as_view(), name="Student"),
    path("faculty/", FacultyDetailView.as_view(), name="Faculty"),
]

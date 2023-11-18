from django.urls import path, include
from .views import (
    BatchDetailView,
    StudentListView,
    UserDetailsView,
    SemesterViewSet,
    CourseViewSet,
    BranchViewSet,
    BatchStudentDetailsView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"semesters", SemesterViewSet, basename="semester")
router.register(r"courses", CourseViewSet, basename="courses")
router.register(r"branches", BranchViewSet, basename="branches")

urlpatterns = [
    path("batch/", BatchDetailView.as_view()),
    path("batch/student/<int:pk>", StudentListView.as_view()),
    path("user/", UserDetailsView.as_view()),
    path("batch-student/<str:roll>", BatchStudentDetailsView.as_view()),
    path("", include(router.urls)),
]

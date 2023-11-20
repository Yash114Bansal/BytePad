from django.urls import path, include
from .views import (
    BatchDetailView,
    StudentListView,
    UserDetailsView,
    SemesterViewSet,
    CourseViewSet,
    BranchViewSet,
    SlotViewSets,
    BatchStudentDetailsView,
    StudentCoursesView
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"semesters", SemesterViewSet, basename="semester")
router.register(r"courses", CourseViewSet, basename="courses")
router.register(r"branches", BranchViewSet, basename="branches")
router.register(r"slots", SlotViewSets, basename="slots")

urlpatterns = [
    path("batch/", BatchDetailView.as_view()),
    path("batch/student/<int:pk>", StudentListView.as_view()),
    path("user/", UserDetailsView.as_view()),
    path("batch-student/<str:roll>", BatchStudentDetailsView.as_view()),
    path("student/mycourses/",StudentCoursesView.as_view()),
    path("", include(router.urls)),
]

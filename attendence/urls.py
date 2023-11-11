from django.urls import path
from .views import (
    AttendenceSheetCreateView,
    AttendenceSheetDeleteView,
    FacultyBatchAttendanceView,
    StudentAttendanceView,
    AttendanceUpdateView,
)

urlpatterns = [
    path("sheet/create/", AttendenceSheetCreateView.as_view(), name="attendance-sheet-create"),
    path("sheet/delete/<int:pk>", AttendenceSheetDeleteView.as_view(), name="attendance-sheet-delete"),
    path('faculty/<int:batch_id>/', FacultyBatchAttendanceView.as_view(), name='faculty-batch-attendance'),
    path('update/<int:pk>',AttendanceUpdateView.as_view(),name='update-attendance'),
    path("student/",StudentAttendanceView.as_view(), name='studeny-attendance')

]

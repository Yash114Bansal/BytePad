from django.urls import path
from .views import (
    AttendanceSheetCreateView,
    AttendanceSheetDeleteView,
    FacultyBatchAttendanceView,
    StudentAttendanceView,
    AttendanceUpdateView,
)

urlpatterns = [
    path("sheet/create/", AttendanceSheetCreateView.as_view(), name="attendance-sheet-create"),
    path("sheet/delete/<int:pk>", AttendanceSheetDeleteView.as_view(), name="attendance-sheet-delete"),
    path('faculty/<int:batch_id>/', FacultyBatchAttendanceView.as_view(), name='faculty-batch-attendance'),
    path('update/<int:pk>',AttendanceUpdateView.as_view(),name='update-attendance'),
    path("student/",StudentAttendanceView.as_view(), name='studeny-attendance')

]

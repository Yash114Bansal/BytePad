from django.urls import path
from .views import AttendenceSheetCreateView,AttendenceSheetDeleteView

urlpatterns = [
    path("sheet/create/", AttendenceSheetCreateView.as_view(), name="attendance-sheet-create"),
    path("sheet/delete/<int:pk>", AttendenceSheetDeleteView.as_view(), name="attendance-sheet-delete"),
]

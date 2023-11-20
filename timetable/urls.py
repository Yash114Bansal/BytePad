from django.urls import path
from .views import LectureCreateView, TimeTableView

urlpatterns = [
    path('create/<int:batch_id>/lecture/', LectureCreateView.as_view(), name='lecture-create'),
    path('create/<int:batch_id>/lecture/<int:pk>/', LectureCreateView.as_view(), name='lecture-update'),
    path('',TimeTableView.as_view()),
]

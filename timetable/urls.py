from django.urls import path
from .views import LectureCreateView, LectureUpdateView, TimeTableView, AllTimeTablesView, SubjectDetailsView

urlpatterns = [
    path('create/<int:batch_id>/lecture/', LectureCreateView.as_view(), name='lecture-create'),
    path('create/<int:batch_id>/lecture/<int:pk>/', LectureUpdateView.as_view(), name='lecture-update'),
    path("details/subjects/<batchID>",SubjectDetailsView.as_view()),
    path("all/",AllTimeTablesView.as_view()),
    path('',TimeTableView.as_view()),
]

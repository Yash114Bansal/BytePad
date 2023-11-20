from django.urls import path
from .views import (
    LectureCreateView,
    LectureUpdateView,
    TimeTableView,
    AllTimeTablesView,
    SubjectDetailsView,
    BatchDetailsView,
    LectureDeleteView,
)

urlpatterns = [
    
    path('create/<int:batch_id>/lecture/', LectureCreateView.as_view(), name='lecture-create'),
    path('create/<int:batch_id>/lecture/<int:pk>/', LectureUpdateView.as_view(), name='lecture-update'),
    path('lectures/<int:pk>/', LectureDeleteView.as_view(), name='lecture-delete'),
    
    path("details/batches/", BatchDetailsView.as_view(), name='batch-details'),
    path("details/subjects/<int:batch_id>", SubjectDetailsView.as_view(), name='subject-details'),
    
    path("all/", AllTimeTablesView.as_view(), name='all-timetables'),
    path('', TimeTableView.as_view(), name='timetable'),
]

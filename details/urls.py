from django.urls import path
from .views import BatchDetailView,StudentListView,UserDetailsView

urlpatterns = [
    path("batch/",BatchDetailView.as_view()),
    path("batch/student/<int:pk>",StudentListView.as_view()),
    path("user/",UserDetailsView.as_view())
]

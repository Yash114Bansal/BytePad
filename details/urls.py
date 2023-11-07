from django.urls import path
from .views import BatchDetailView

urlpatterns = [
    path("batch/",BatchDetailView.as_view())
]

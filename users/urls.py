from django.urls import path
from . import views

urlpatterns = [
    path("",views.UserDetailsView.as_view())
]

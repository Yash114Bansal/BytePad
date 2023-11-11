# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SamplePaperViewSet

router = DefaultRouter()
router.register(r'', SamplePaperViewSet, basename='samplepaper')

urlpatterns = [
    path('', include(router.urls)),
]

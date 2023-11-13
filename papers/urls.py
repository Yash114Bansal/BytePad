# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SamplePaperViewSet,SolutionViewSets

router = DefaultRouter()
router.register(r'solutions', SolutionViewSets, basename='samplepaper-solution')
router.register(r'', SamplePaperViewSet, basename='samplepaper')

urlpatterns = [
    path('', include(router.urls)),
]

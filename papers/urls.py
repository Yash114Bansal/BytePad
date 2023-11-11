# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SamplePaperViewSet,SolutionViewSets

router = DefaultRouter()
router.register(r'', SamplePaperViewSet, basename='samplepaper')
router.register(r'solutions', SolutionViewSets, basename='samplepaper-solution')

urlpatterns = [
    path('', include(router.urls)),
]

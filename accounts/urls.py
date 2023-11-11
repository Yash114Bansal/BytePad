from rest_framework.routers import DefaultRouter
from .views import UserViewSet, StudentDetailViewSet, FacultyDetailViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'student', StudentDetailViewSet, basename='student')
router.register(r'faculty', FacultyDetailViewSet, basename='faculty')

urlpatterns = router.urls
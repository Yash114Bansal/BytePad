from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from .models import UserProfile, StudentModel, FacultyModel
from .serializers import UserSerializer, StudentSerializer, FacultySerializer


class UserViewSet(ModelViewSet):

    """
    User Profiles, Admin Access Only
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]


class StudentDetailViewSet(ModelViewSet):

    """
    Student Profiles, Admin Access Only
    """

    queryset = StudentModel.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]


class FacultyDetailViewSet(ModelViewSet):

    """
    Faculty, Admin Access Only
    """

    queryset = FacultyModel.objects.all()
    serializer_class = FacultySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser

from .models import UserProfile, StudentModel, FacultyModel
from .serializers import UserSerializer, StudentDetailSerializer, FacultySerializer


class UserViewSet(ModelViewSet):

    """
    Admin Access Only.

    API Endpoints To Add/Update Users.
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]


class StudentDetailViewSet(ModelViewSet):

    """
    Admin Access Only.

    API Endpoints To Add/Update Student Profiles.
    """

    queryset = StudentModel.objects.all()
    serializer_class = StudentDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]


class FacultyDetailViewSet(ModelViewSet):

    """
    Admin Access Only.

    API Endpoints To Add/Update Faculty Profiles.
    """

    queryset = FacultyModel.objects.all()
    serializer_class = FacultySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

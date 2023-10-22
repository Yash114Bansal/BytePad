from rest_framework import generics
from .models import UserProfile, StudentModel, FacultyModel
from .serializers import UserSerializer, StudentSerializer, FacultySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser

class UserListCreateView(generics.ListCreateAPIView,generics.DestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

class StudentDetailView(generics.ListCreateAPIView):
    queryset = StudentModel.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

class FacultyDetailView(generics.ListCreateAPIView):
    queryset = FacultyModel.objects.all()
    serializer_class = FacultySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

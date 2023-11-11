from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.models import Batch, UserProfile, StudentModel, FacultyModel, Semester, Course, Branch
from accounts.permissions import IsFaculty,IsAdminOrReadOnly
from accounts.serializers import UserSerializer, StudentSerializer, FacultySerializer
from .serializers import BatchDetailSerializer, StudentSerializer,  CourseSerializer,SemeterSerializer,BranchSerializer

class BatchDetailView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFaculty]

    def get(self, request):
        user_email = request.user.email

        active_batches_with_faculty = Batch.objects.filter(is_active=True).filter(
            Q(batchcoursefacultyassignment__faculty__user=user_email)
        )

        if active_batches_with_faculty:
            serializer = BatchDetailSerializer(active_batches_with_faculty, many=True)
            return Response(serializer.data)

        else:
            return Response(
                {"message": "No active batches with faculty found."}, status=404
            )


class StudentListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFaculty]

    def get(self, request, pk, *args, **kwargs):
        try:
            batch = Batch.objects.get(pk=pk)
        except Batch.DoesNotExist:
            return Response({"message": "Batch not found"}, status=404)

        batch_students = batch.students.all()
        serializer = StudentSerializer(batch_students, many=True)

        if serializer.is_valid:
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            # Getting User With Corresponding ID
            user = UserProfile.objects.get(email=request.user.email)

            serializer = UserSerializer(user)

            additional_data = {}

            # If The User Is A Faculty, Include Faculty Details
            if user.is_faculty:
                faculty = FacultyModel.objects.get(user=user.email)
                faculty_serializer = FacultySerializer(faculty)
                additional_data = faculty_serializer.data

            # If The User Is A Student, Include Student Details
            if user.is_student:
                student = StudentModel.objects.get(user=user.email)
                student_serializer = StudentSerializer(student)
                additional_data = student_serializer.data

            # Merge The Additional Data Into The User Data
            response_data = {**serializer.data, **additional_data}

            # Return The Response With A Status Code Of 200
            return Response(response_data, status=status.HTTP_200_OK)

        # If User Profile Does Not Exists
        except UserProfile.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        # If User Is Faculty And Faculty Details Does Not Exists
        except FacultyModel.DoesNotExist:
            return Response(
                {"message": "Faculty data not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # If User Is Student And Student Details Does Not Exists
        except StudentModel.DoesNotExist:
            return Response(
                {"message": "Student data not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

class SemesterViewSet(ModelViewSet):
    queryset = Semester.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = SemeterSerializer

class BranchViewSet(ModelViewSet):
    queryset = Branch.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = BranchSerializer

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CourseSerializer
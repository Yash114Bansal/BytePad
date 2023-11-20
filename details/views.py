from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.permissions import IsFaculty, IsAdminOrReadOnly, IsStudent
from accounts.serializers import UserSerializer, StudentDetailSerializer, FacultySerializer
from accounts.models import (
    Batch,
    UserProfile,
    StudentModel,
    BatchCourseFacultyAssignment,
    FacultyModel,
    Semester,
    Course,
    Branch,
)
from timetable.models import LectureNumberModel
from .serializers import (
    BatchDetailSerializer,
    StudentSerializer,
    CourseSerializer,
    SemeterSerializer,
    BranchSerializer,
    StudentCoursesSerializer,
    LectureNumberSerializer,
)


class BatchDetailView(APIView):

    """
    Get Details Of Batch (Faculty).

    API endpoint for Getting Batches Of Faculty
    """

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

    """
    Get List Of Students Of Batch (Faculty).

    API Endpoint To Get List Of Students in a Batch.
    
    *Requires Batch ID
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFaculty]

    def get(self, request, pk, *args, **kwargs):
        try:
            batch = Batch.objects.get(pk=pk)
        except Batch.DoesNotExist:
            return Response({"message": "Batch not found"}, status=404)

        batch_students = batch.students.all()
        serializer = StudentSerializer(batch_students, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailsView(APIView):

    """
    Get Details(Student / Faculty).

    API Endpoint For Getting Details of User.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            # Getting User With Corresponding ID
            user = request.user

            serializer = UserSerializer(user)

            additional_data = {}

            # If The User Is A Faculty, Include Faculty Details
            if user.is_faculty:
                faculty = FacultyModel.objects.get(user=user)
                faculty_serializer = FacultySerializer(faculty)
                additional_data = faculty_serializer.data

            # If The User Is A Student, Include Student Details
            if user.is_student:
                student = StudentModel.objects.get(user=user)
                student_serializer = StudentDetailSerializer(student)
                additional_data = student_serializer.data
                additional_data.pop("user",None)

            # Merge The Additional Data Into The User Data
            response_data = {**serializer.data, **additional_data}

            # Return The Response With A Status Code Of 200
            return Response(response_data, status=status.HTTP_200_OK)

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

class BatchStudentDetailsView(APIView):

    """
    Get Details Of Student Of A Batch (Faculty).

    API Endpoint For Getting Details Student Of A Batch.

    *Requires Roll Number Of Student.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFaculty]

    def get(self, request, roll ,*args, **kwargs):
        try:
            # Getting User With Corresponding ID
            student = StudentModel.objects.get(roll_number=roll)


            serializer = UserSerializer(student.user)

            additional_data = {}

            student_serializer = StudentDetailSerializer(student)
            additional_data = student_serializer.data
            additional_data.pop("user",None)
            
            # Merge The Additional Data Into The User Data
            response_data = {**serializer.data, **additional_data}

            # Return The Response With A Status Code Of 200
            return Response(response_data, status=status.HTTP_200_OK)

        # If User Profile Does Not Exists
        except UserProfile.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST
            )


        # If User Is Student And Student Details Does Not Exists
        except StudentModel.DoesNotExist:
            return Response(
                {"message": "Student data not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

class StudentCoursesView(APIView):
    """
    Get Courses (Student).

    API Endpoint For Students To See Their Courses.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudent]

    def get(self, request):
        user = request.user

        # Getting Student Model
        student = StudentModel.objects.get(user=user)

        # Filtering Courses For Student
        courses = BatchCourseFacultyAssignment.objects.filter(
            batch__is_active=True,
            batch__students__in=[student]
        )
        serializer = StudentCoursesSerializer(courses,many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SemesterViewSet(ModelViewSet):

    """
    Get List Of Semesters (Student / Faculty).

    API Endpoint For Getting Details Of Semester.
    (Only Admin Can Update).
    """

    queryset = Semester.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = SemeterSerializer


class BranchViewSet(ModelViewSet):

    """
    Get List Of Branches And Their Details (Student / Faculty).

    API Endpoint For Getting Details Of Branches
    (Only Admin Can Update)
    """

    queryset = Branch.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = BranchSerializer


class CourseViewSet(ModelViewSet):

    """
    Get List Of Courses And Their Details (Student / Faculty).

    API Endpoint For Getting Details Of Courses
    (Only Admin Can Update)
    """

    queryset = Course.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CourseSerializer

class SlotViewSets(ModelViewSet):
    """
    Get List Of Time Table Slots (Student / Faculty).

    API Endpoint For Getting Details Of Time Table Slots
    (Only Admin Can Update)
    """

    queryset = LectureNumberModel.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = LectureNumberSerializer
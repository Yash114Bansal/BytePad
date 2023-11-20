from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Cast
from django.db.models import TextField

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from accounts.models import (
    Batch,
    StudentModel,
    FacultyModel,
    BatchCourseFacultyAssignment,
)
from accounts.permissions import IsHOD
from .models import LectureModel, TimeTableModel
from .serializers import (
    LectureCreateSerializer,
    StudentLectureViewSerializer,
    FacultyLectureViewSerializer,
    AllTimeTablesSerializer,
    SubjectDetailsSerializer,
    BatchDetailsSerializer,
)


class LectureCreateView(generics.CreateAPIView):
    """
    Create Time Table (HOD only)

    API Endpoint To Add Lectures Of Time Table
    """

    queryset = LectureModel.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsHOD]
    serializer_class = LectureCreateSerializer

    def create(self, request, *args, **kwargs):
        batch_id = kwargs.get("batch_id")
        try:
            batch = Batch.objects.get(pk=batch_id)
        except Batch.DoesNotExist:
            return Response(
                {"detail": f"Batch with ID {batch_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lecture = serializer.save()

        timetable, created = TimeTableModel.objects.get_or_create(batch=batch)
        timetable.lectures.add(lecture)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class LectureUpdateView(generics.UpdateAPIView):
    """
    Update Time Table (HOD only)

    API Endpoint To Add Lectures Of Time Table
    """

    queryset = LectureModel.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsHOD]
    serializer_class = LectureCreateSerializer

    def update(self, request, *args, **kwargs):
        batch_id = kwargs.get("batch_id")
        lecture_id = kwargs.get("pk")
        try:
            batch = Batch.objects.get(pk=batch_id)
            lecture = LectureModel.objects.get(pk=lecture_id)
        except Batch.DoesNotExist:
            return Response(
                {"detail": f"Batch with ID {batch_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except LectureModel.DoesNotExist:
            return Response(
                {"detail": f"Lecture with ID {lecture_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(lecture, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class LectureDeleteView(generics.DestroyAPIView):
    """
    Delete a Lecture (HOD only)

    API Endpoint To Delete a Lecture
    """

    queryset = LectureModel.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsHOD]

    def destroy(self, request, *args, **kwargs):
        lecture_id = kwargs.get("pk")
        lecture = get_object_or_404(LectureModel, pk=lecture_id)
        lecture.delete()
        return Response(
            {"detail": "Lecture deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class TimeTableView(APIView):

    """
    Get Your TimeTable (Student / Faculty)

    API Endpoint To Get Time Table
    """

    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "day",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=[
                    "monday",
                    "tuesday",
                    "wednesday",
                    "thursday",
                    "friday",
                    "saturday",
                    "sunday",
                ],
                description="Filter by day of the week",
            )
        ]
    )
    def get(self, request):

        user = request.user

        if user.is_student:

            student = StudentModel.objects.get(user=user)
            batch = Batch.objects.filter(is_active=True, students=student).first()
            timetable = TimeTableModel.objects.get(batch=batch)

            lectures = timetable.lectures.all()

            day = request.query_params.get("day")

            if day:
                lectures = lectures.filter(day=day)

            serializer = StudentLectureViewSerializer(lectures, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        if user.is_faculty:

            faculty = FacultyModel.objects.get(user=user)

            assignments = BatchCourseFacultyAssignment.objects.filter(faculty=faculty)

            lectures = LectureModel.objects.filter(subject__in=assignments)

            day = request.query_params.get("day")

            if day:
                lectures = lectures.filter(day=day)

            serializer = FacultyLectureViewSerializer(lectures, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)


class AllTimeTablesView(APIView):
    """
    Get All TimeTables (HOD only)

    API Endpoint To Add Lectures Of Time Table
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsHOD]
    pagination_class = PageNumberPagination

    SIMILARITY_THRESHOLD = 0.1

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "batchName",
                openapi.IN_QUERY,
                description="Filter Time Tables On Basis Of Batches Name",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        queryset = TimeTableModel.objects.all()
        query = self.request.query_params.get("batchName", None)

        if query:
            batch_name_similarity = TrigramSimilarity(
                Cast("batch__name", output_field=TextField()), query
            )
            queryset = (
                TimeTableModel.objects.annotate(similarity=batch_name_similarity)
                .filter(similarity__gt=self.SIMILARITY_THRESHOLD)
                .order_by("-similarity")
            )

        serializer = AllTimeTablesSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubjectDetailsView(APIView):
    """
    Get Details Of Subjects (HOD only)

    API Endpoint To Get Details Of Subjects From Batch ID
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsHOD]

    def get(self, request, batchID):
        assignments = BatchCourseFacultyAssignment.objects.filter(batch=batchID)
        serializer = SubjectDetailsSerializer(assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BatchDetailsView(APIView):
    """
    Get Details Of Batches (HOD only)

    API Endpoint To Get Details Of All Batches
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsHOD]
    SIMILARITY_THRESHOLD = 0.1

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "batchName",
                openapi.IN_QUERY,
                description="Filter Batches On Basis Of Name",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def get(self, request):
        batches = Batch.objects.filter(is_active=True)
        query = self.request.query_params.get("batchName", None)

        if query:
            batch_name_similarity = TrigramSimilarity(
                Cast("name", output_field=TextField()), query
            )
            batches = (
                Batch.objects.annotate(similarity=batch_name_similarity)
                .filter(similarity__gt=self.SIMILARITY_THRESHOLD)
                .order_by("-similarity")
            )
        serializer = BatchDetailsSerializer(batches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

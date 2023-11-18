from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Cast
from django.db.models import TextField
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from accounts.permissions import IsHODOrReadOnly, IsFacultyOrReadOnly
from .models import SamplePaper, SamplePaperSolution, MyCollections
from .serializers import (
    SamplePaperSerializer,
    SolutionSerializer,
    MyCollectionsSerailizer,
)


class SamplePaperViewSet(viewsets.ModelViewSet):
    """
    Get Sample Papers.

    API Endpoint For Sample Papers Students, Faculty Can View, Only HODs Can Update.
    """

    queryset = SamplePaper.objects.all()
    serializer_class = SamplePaperSerializer
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsHODOrReadOnly]
    pagination_class = PageNumberPagination
    SIMILARITY_THRESHOLD = 0.1

    def get_queryset(self):
        """
        Filtering Results
        """

        query = self.request.query_params.get("search")
        year = self.request.query_params.get("year")
        semester = self.request.query_params.get("semester")
        course_code = self.request.query_params.get("course_code")

        if query:
            title_similarity = TrigramSimilarity(
                Cast("title", output_field=TextField()), query
            )
            queryset = (
                SamplePaper.objects.annotate(similarity=title_similarity)
                .filter(similarity__gt=self.SIMILARITY_THRESHOLD)
                .order_by("-similarity")
            )
        else:
            queryset = super().get_queryset()

        if year:
            queryset = queryset.filter(year=year)

        if semester:
            queryset = queryset.filter(semester=semester)

        if course_code:
            queryset = queryset.filter(courses__course_code=course_code)

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Filter papers based on the provided search query",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "year",
                openapi.IN_QUERY,
                description="Filter papers based on year",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "semester",
                openapi.IN_QUERY,
                description="Filter papers based on semester",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "course_code",
                openapi.IN_QUERY,
                description="Filter papers based on course code",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class SolutionViewSets(viewsets.ModelViewSet):
    """
    Get Solutions.

    API Endpoint For Sample Paper Solutions. Students Can Read, Faculties Can Update.
    """

    queryset = SamplePaperSolution.objects.all()
    serializer_class = SolutionSerializer
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFacultyOrReadOnly]
    pagination_class = PageNumberPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "paper_id",
                openapi.IN_QUERY,
                description="Filter solutions based on the provided paper ID",
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):

        """
        Filtering Results
        """

        paper_id = self.request.query_params.get("paper_id")

        if paper_id:
            queryset = SamplePaperSolution.objects.filter(paper=paper_id)
        else:
            queryset = super().get_queryset()

        return queryset


class MyCollectionsViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet,
):

    """
    Collections (Student / Faculty).

    API endpoint for Collections.
    """

    queryset = MyCollections.objects.all()
    serializer_class = MyCollectionsSerailizer
    authentication_classes = [JWTAuthentication]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = MyCollections.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

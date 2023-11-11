from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Cast
from django.db.models import TextField
from accounts.permissions import IsHODOrReadOnly,IsFacultyOrReadOnly

from .models import SamplePaper,SamplePaperSolution
from .serializers import SamplePaperSerializer,SolutionSerializer

class SamplePaperViewSet(viewsets.ModelViewSet):
    """
    API endpoint for sample papers .

    Use the following query parameters for filtering (in GET):
    - `search`: Filter papers based on the provided search query.
    
    - `year`: Filter papers based on year.
    
    - `semester`: Filter papers based on semester.
    
    - `course_code`: Filter papers based on course.
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

        query = self.request.query_params.get('search')
        year = self.request.query_params.get('year')
        semester = self.request.query_params.get('semester')
        course_code = self.request.query_params.get('course_code')

        if query:
            title_similarity = TrigramSimilarity(Cast('title', output_field=TextField()), query)
            queryset = SamplePaper.objects.annotate(similarity=title_similarity).filter(similarity__gt=self.SIMILARITY_THRESHOLD).order_by('-similarity')
        else:
            queryset = super().get_queryset()

        if year:
            queryset = queryset.filter(year=year)

        if semester:
            queryset = queryset.filter(semester=semester)

        if course_code:
            queryset = queryset.filter(courses__course_code=course_code)

        return queryset

class SolutionViewSets(viewsets.ModelViewSet):
    """
    API endpoint for  sample papers solutions.

    Use the following query parameters for filtering:
    - `paper_id`: Filter solutions based on the provided paper ID.
    """
    queryset = SamplePaperSolution.objects.all()
    serializer_class = SolutionSerializer
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFacultyOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """
        Filtering Results
        """

        paper_id = self.request.query_params.get('paper_id')

        if paper_id:
            queryset = SamplePaperSolution.objects.filter(paper_id=paper_id)
        else:
            queryset = super().get_queryset()

        return queryset
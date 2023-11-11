from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Cast
from django.db.models import TextField
from .models import SamplePaper
from .serializers import SamplePaperSerializer
from .permissions import IsHODOrReadOnly

class SamplePaperViewSet(viewsets.ModelViewSet):
    """
    API endpoint for uploading sample papers.
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

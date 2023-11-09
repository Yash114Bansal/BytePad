from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Cast
from django.db.models import TextField
from .models import SamplePaper
from .serializers import SamplePaperUploadSerializer
from .permissions import IsFacultyOrReadOnly


class FileUploadViewSet(viewsets.ModelViewSet):

    """
    API endpoint for uploading sample papers.
    """

    queryset = SamplePaper.objects.all()
    serializer_class = SamplePaperUploadSerializer
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFacultyOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):

        """
        Filtering Results
        """

        query = self.request.query_params.get('search')
        year_param = self.request.query_params.get('year')
        semester_param = self.request.query_params.get('semester')
        course_code_param = self.request.query_params.get('course_code')

        if query:

            title_similarity = TrigramSimilarity(Cast('title', output_field=TextField()), query)
            print(title_similarity)
            queryset = SamplePaper.objects.annotate(similarity=title_similarity).order_by('-similarity')
            for item in queryset:
                print(item.similarity)
        else:
            queryset = super().get_queryset()

        if year_param:
            queryset = queryset.filter(year=year_param)

        if semester_param:
            queryset = queryset.filter(semester=semester_param)
            
        if course_code_param:
            queryset = queryset.filter(courses__course_code=course_code_param)

        return queryset
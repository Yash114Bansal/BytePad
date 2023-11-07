from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets
from .models import SamplePaper
from .serializers import SamplePaperUploadSerializer
from .permissions import IsFacultyOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Cast
from django.db.models import TextField

class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = SamplePaper.objects.all()
    serializer_class = SamplePaperUploadSerializer
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFacultyOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        query = self.request.query_params.get('search')

        if query:
            print(query)
            title_similarity = TrigramSimilarity(Cast('title', output_field=TextField()), query)
            overall_similarity = title_similarity 

            queryset = SamplePaper.objects.annotate(similarity=overall_similarity).filter(similarity__gt=0.3).order_by('-similarity')
           
        else:
            queryset = super().get_queryset()

        return queryset
from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets
from .models import SamplePaper
from .serializers import SamplePaperUploadSerializer
from .permissions import IsFacultyOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination


class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = SamplePaper.objects.all()
    serializer_class = SamplePaperUploadSerializer
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFacultyOrReadOnly]
    pagination_class = PageNumberPagination


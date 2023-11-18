from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone

from accounts.permissions import IsHODOrReadOnly
from .models import Announcement, BatchSpecificAnnouncement
from .serializers import AnnouncementListSerializer,AnnouncementCreateSerializer, BatchSpecificAnnouncementSerializer

class AnnouncementCreateView(generics.CreateAPIView):
    queryset = Announcement.objects.all()
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsHODOrReadOnly]
    serializer_class = AnnouncementCreateSerializer

    def perform_create(self, serializer):

        serializer.save(author=self.request.user)

class AnnouncementListView(generics.ListAPIView):
    queryset = Announcement.objects.filter(time__gte=timezone.now())
    serializer_class = AnnouncementListSerializer
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):

        announcements =  Announcement.objects.filter(time__gte=timezone.now()).order_by('time')

        if self.request.user.is_student:
            announcements =  Announcement.objects.filter(faculty_only = False)
        
        return announcements
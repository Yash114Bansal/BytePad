from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from django.utils import timezone

from accounts.models import BatchCourseFacultyAssignment, StudentModel
from accounts.permissions import IsHODOrReadOnly, IsFaculty, IsStudent
from .models import Announcement, BatchSpecificAnnouncement
from .serializers import (
    AnnouncementListSerializer,
    AnnouncementCreateSerializer,
    BatchSpecificAnnouncementCreateSerializer,
    BatchSpecificAnnouncementListSerializer,
)


class AnnouncementCreateView(generics.CreateAPIView):
    """
    Create Announcements (HODs).

    API Endpoint For HODs To Create Announcements.
    """

    queryset = Announcement.objects.all()
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsHODOrReadOnly]
    serializer_class = AnnouncementCreateSerializer

    def perform_create(self, serializer):

        serializer.save(author=self.request.user)


class AnnouncementListView(generics.ListAPIView):
    """
    View HOD Announcements.

    API Endpoint TO View Announcements By HODs.
    """

    queryset = Announcement.objects.all()
    serializer_class = AnnouncementListSerializer
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):

        # Filtering And Ordering Announcements By Time
        announcements = Announcement.objects.filter(time__gte=timezone.now()).order_by(
            "time"
        )

        if self.request.user.is_student:

            # Removing Faculty-Only Announcements
            announcements = Announcement.objects.filter(faculty_only=False)

        return announcements


class BatchSpecificAnnouncementCreateView(generics.CreateAPIView):
    """
    Create Batch Announcements (Faculties).

    API Endpoint For Faculty To Create Announcement For Their Batch.
    """

    queryset = BatchSpecificAnnouncement.objects.all()
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFaculty]
    serializer_class = BatchSpecificAnnouncementCreateSerializer

    def perform_create(self, serializer):
        batch_id = serializer.validated_data["Batch"]
        try:
            # Checking If Faculty Gave ID of His Own Batch
            BatchCourseFacultyAssignment.objects.get(
                batch=batch_id, faculty=self.request.user.facultymodel_set.first()
            )
        except BatchCourseFacultyAssignment.DoesNotExist:
            raise ValidationError({"message": "Invalid Batch For The Faculty"})

        serializer.save(author=self.request.user)


class BatchSpecificAnnouncementListView(generics.ListAPIView):
    """
    View Batch Announcements (Students).

    API Endpoint For Student To View Announcement of Faculties.
    """

    queryset = BatchSpecificAnnouncement.objects.all()
    serializer_class = BatchSpecificAnnouncementListSerializer
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudent]

    def get_queryset(self):

        student = StudentModel.objects.get(user=self.request.user)

        # Filtering And Ordering Announcements By Time
        announcements = BatchSpecificAnnouncement.objects.filter(
            time__gte=timezone.now(), Batch__students__in=[student]
        ).order_by("time")

        return announcements

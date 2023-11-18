from .models import Announcement, BatchSpecificAnnouncement
from rest_framework import serializers


class AnnouncementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = [
            "author",
            "title",
            "document",
            "description",
            "time",
            "venue",
            "faculty_only",
        ]


class AnnouncementCreateSerializer(serializers.ModelSerializer):
    document = serializers.FileField(required=False)
    venue = serializers.CharField(required=False)

    class Meta:
        model = Announcement
        fields = ["title", "document", "description", "time", "venue", "faculty_only"]


class BatchSpecificAnnouncementListSerializer(serializers.ModelSerializer):
    batch_name = serializers.CharField(source="Batch.name")

    class Meta:
        model = BatchSpecificAnnouncement
        fields = ["batch_name", "title", "document", "description", "time", "venue"]


class BatchSpecificAnnouncementCreateSerializer(serializers.ModelSerializer):
    document = serializers.FileField(required=False)
    venue = serializers.CharField(required=False)

    class Meta:
        model = BatchSpecificAnnouncement
        fields = ["Batch", "title", "document", "description", "time", "venue"]

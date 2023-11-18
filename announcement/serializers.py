from rest_framework import serializers
from .models import Announcement, BatchSpecificAnnouncement
from rest_framework import serializers

class AnnouncementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ["author","title", "document", "description", "time", "venue", "faculty_only"]


class AnnouncementCreateSerializer(serializers.ModelSerializer):
    document = serializers.FileField(required=False)
    class Meta:
        model = Announcement
        fields = ["title", "document", "description", "time", "venue", "faculty_only"]
    


class BatchSpecificAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchSpecificAnnouncement
        fields = '__all__'

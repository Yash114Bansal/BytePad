from rest_framework import serializers
from .models import LectureModel

class LectureCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureModel
        fields = "__all__"

class StudentLectureViewSerializer(serializers.ModelSerializer):
    start_time = serializers.CharField(source="slot_number.start_time")
    end_time = serializers.CharField(source="slot_number.end_time")
    teacher = serializers.CharField(source="subject.faculty.user.name")
    course_name = serializers.CharField(source="subject.course.name")
    course_code = serializers.CharField(source="subject.course.course_code")
    class Meta:
        model = LectureModel
        fields = ["start_time","end_time","day","teacher","course_name","course_code","room"]

        
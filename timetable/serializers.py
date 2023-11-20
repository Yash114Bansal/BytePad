from rest_framework import serializers
from .models import LectureModel, TimeTableModel
from accounts.models import BatchCourseFacultyAssignment, Batch


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
        fields = [
            "start_time",
            "end_time",
            "day",
            "teacher",
            "course_name",
            "course_code",
            "room",
        ]


class FacultyLectureViewSerializer(serializers.ModelSerializer):
    start_time = serializers.CharField(source="slot_number.start_time")
    end_time = serializers.CharField(source="slot_number.end_time")
    course_name = serializers.CharField(source="subject.course.name")
    course_code = serializers.CharField(source="subject.course.course_code")
    batch_name = serializers.CharField(source="subject.batch.name")

    class Meta:
        model = LectureModel
        fields = [
            "start_time",
            "end_time",
            "day",
            "batch_name",
            "course_name",
            "course_code",
            "room",
        ]


class AllLectureViewSerializer(serializers.ModelSerializer):
    start_time = serializers.CharField(source="slot_number.start_time")
    end_time = serializers.CharField(source="slot_number.end_time")
    teacher = serializers.CharField(source="subject.faculty.user.name")
    course_name = serializers.CharField(source="subject.course.name")
    course_code = serializers.CharField(source="subject.course.course_code")

    class Meta:
        model = LectureModel
        fields = [
            "id",
            "start_time",
            "end_time",
            "day",
            "teacher",
            "course_name",
            "course_code",
            "room",
        ]


class AllTimeTablesSerializer(serializers.ModelSerializer):
    batch_name = serializers.CharField(source="batch.name")
    lectures = AllLectureViewSerializer(many=True)

    class Meta:
        model = TimeTableModel
        fields = ["batch", "batch_name", "lectures"]


class SubjectDetailsSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.name")
    course_code = serializers.CharField(source="course.course_code")
    teacher = serializers.CharField(source="faculty.user.name")

    class Meta:
        model = BatchCourseFacultyAssignment
        fields = ["id", "course_name", "course_code", "teacher"]


class BatchDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ["id", "name"]

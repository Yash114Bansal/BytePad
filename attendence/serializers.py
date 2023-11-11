from rest_framework import serializers
from accounts.models import FacultyModel, BatchCourseFacultyAssignment,Batch
from .models import Attendance, AttendanceSheet

class AttendanceSerializer(serializers.ModelSerializer):
    roll_number = serializers.ReadOnlyField(source='student.roll_number')
    class Meta:
        model = Attendance
        fields = ["roll_number","date","present"]


class AttendanceSheetSerializer(serializers.Serializer):
    batchID = serializers.IntegerField()
    all_present = serializers.BooleanField(default=False)
    date = serializers.DateField()

    def create(self, validated_data):

        date = validated_data["date"]
        batch = validated_data["batchID"]
        all_present = validated_data["all_present"]

        user = self.context["request"].user

        try:
            faculty = FacultyModel.objects.get(user=user)
            batchCourseObject = BatchCourseFacultyAssignment.objects.get(
                faculty=faculty, batch=batch
            )

        except FacultyModel.DoesNotExist:
            raise serializers.ValidationError({"message": "Faculty Not Found"})
        except BatchCourseFacultyAssignment.DoesNotExist:
            raise serializers.ValidationError(
                {"message": "Invalid Batch For the Provided Faculty"}
            )

        existing_attendance_sheet = AttendanceSheet.objects.filter(
            assignment=batchCourseObject, date=date
        ).first()
        if existing_attendance_sheet:
            raise serializers.ValidationError(
                {"message": "AttendanceSheet already exists for this date"}
            )

        students = batchCourseObject.batch.students.all()

        attendance_records = [
            Attendance(student=student, date=date, present=all_present)
            for student in students
        ]

        created_attendance_records = Attendance.objects.bulk_create(attendance_records)

        attendance_sheet = AttendanceSheet.objects.create(
            assignment=batchCourseObject, date=date
        )
        attendance_sheet.attendance_records.set(created_attendance_records)
        
        return attendance_sheet

class BatchAttendanceSerializer(serializers.Serializer):
    batchID = serializers.IntegerField()
    date = serializers.DateField()

    def validate_batchID(self, value):
        try:
            batch = Batch.objects.get(pk=value)
        except Batch.DoesNotExist:
            raise serializers.ValidationError("Batch not found.")
        return batch

class FacultyBatchAttendanceSerializer(serializers.Serializer):
    batchID = serializers.IntegerField(source='assignment.batch.id')
    attendance_records = AttendanceSerializer(many=True)
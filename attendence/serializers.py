from rest_framework import serializers
from accounts.models import FacultyModel, BatchCourseFacultyAssignment, Batch
from .models import Attendance, AttendanceSheet


class FacultyAttendanceSerializer(serializers.ModelSerializer):
    roll_number = serializers.ReadOnlyField(source="student.roll_number")

    class Meta:
        model = Attendance
        fields = ["id", "roll_number", "date", "present"]


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

        return attendance_records


class AttendanceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["id", "date", "present"]


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
    batchID = serializers.IntegerField(source="assignment.batch.id")
    attendance_records = FacultyAttendanceSerializer(many=True)


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["student", "present"]


class StudentAttendanceResponseSerializer(serializers.Serializer):
    date = serializers.DateField()
    course_name = serializers.CharField(source="assignment.course.name")
    course_code = serializers.CharField(source="assignment.course.course_code")
    attendance_records = AttendanceSerializer(many=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context.get("user")

        if user and user.is_student:
            student_id = user.studentmodel_set.first().id
            student_records = [
                record
                for record in representation["attendance_records"]
                if record["student"] == student_id
            ]
            for record in student_records:
                record.pop("student", None)

            representation["attendance_records"] = student_records

        return representation

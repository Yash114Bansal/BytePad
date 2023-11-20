from collections import defaultdict
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import date, timedelta
from django.db.models import Count, Case, When, F, Sum, Value, IntegerField, Q
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from accounts.models import Batch, StudentModel, BatchCourseFacultyAssignment
from accounts.permissions import IsFaculty, IsStudent

from .models import Attendance, AttendanceSheet
from .serializers import (
    AttendanceSheetSerializer,
    FacultyBatchAttendanceSerializer,
    StudentAttendanceResponseSerializer,
    AttendanceUpdateSerializer,
    FacultyAttendanceSerializer,
)


class AttendanceSheetCreateView(GenericAPIView):
    """
    Create Attendance Sheet For A Lecture (Faculty).

    Create Bulk Attandance Record Of All Students of Batch.

    - `batchID` : ID Of Batch.

    - `all_present` : Where To Mark Everyone Present Initially.

    - `date` : Date Of Lecture

    """

    queryset = AttendanceSheet.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFaculty]
    serializer_class = AttendanceSheetSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            attendance_records = serializer.save()

            return Response(
                FacultyAttendanceSerializer(attendance_records, many=True).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceSheetDeleteView(GenericAPIView):

    """
    Delete Attendance Sheet (Faculty).

    API Endpoint To Delete Whole Attendance Sheet.
    """

    queryset = AttendanceSheet.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFaculty]

    def delete(self, request, pk):
        try:
            attendance_sheet = AttendanceSheet.objects.get(pk=pk)
        except AttendanceSheet.DoesNotExist:
            return Response(
                {"message": "Attendance sheet not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        attendance_sheet.delete()
        return Response(
            {"message": "Attendance sheet deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class FacultyBatchAttendanceView(ListAPIView):
    """
    View Attendance (Faculty).

    API Endpoint For Faculty To View Attendance Of A Batch.
    > Required:
    - `batchID` : ID Of Batch.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFaculty]
    serializer_class = FacultyBatchAttendanceSerializer

    def get_queryset(self):
        return AttendanceSheet.objects.all()

    def list(self, request, *args, **kwargs):
        batch_id = self.kwargs.get("batch_id")

        try:
            batch = Batch.objects.get(pk=batch_id)
            attendance_sheets = AttendanceSheet.objects.filter(assignment__batch=batch)

            from_date_str = request.query_params.get("from_date")
            to_date_str = request.query_params.get("to_date")
            last_days = request.query_params.get("last_days")
            last_month = request.query_params.get("last_month")

            today = timezone.now().date()

            if from_date_str and to_date_str:
                from_date = date.fromisoformat(from_date_str)
                to_date = date.fromisoformat(to_date_str)
                attendance_sheets = attendance_sheets.filter(
                    date__range=(from_date, to_date)
                )
            elif last_days:
                last_days = int(last_days)
                start_date = today - timedelta(days=last_days)
                attendance_sheets = attendance_sheets.filter(
                    date__range=(start_date, today)
                )
            elif last_month:
                start_date = today - timedelta(days=today.day)
                end_date = today.replace(day=1) - timedelta(days=1)
                attendance_sheets = attendance_sheets.filter(
                    date__range=(start_date, end_date)
                )

        except Batch.DoesNotExist:
            return Response(
                {"message": "batch does not exists"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(attendance_sheets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AttendanceUpdateView(UpdateAPIView):
    """
    Update Attendance (Faculty).

    API Endpoint For Faculty To Update Attendance.
    """

    queryset = Attendance.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFaculty]
    serializer_class = AttendanceUpdateSerializer


class StudentAttendanceView(GenericAPIView):
    """
    View Attendance (Students).

    API Endpoint For Student TO View Their Attendance
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudent]
    serializer_class = StudentAttendanceResponseSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "from_date",
                openapi.IN_QUERY,
                description="Start date of the date range (optional)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                example="2023-01-01",
            ),
            openapi.Parameter(
                "to_date",
                openapi.IN_QUERY,
                description="End date of the date range (optional)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                example="2023-01-31",
            ),
            openapi.Parameter(
                "last_days",
                openapi.IN_QUERY,
                description="Number of days to look back (optional)",
                type=openapi.TYPE_INTEGER,
                example=7,
            ),
            openapi.Parameter(
                "last_month",
                openapi.IN_QUERY,
                description="Filter for the last month (optional)",
                type=openapi.TYPE_BOOLEAN,
                example=True,
            ),
        ],
    )
    def get(self, request):
        user = request.user
        student = StudentModel.objects.get(user=user)

        active_batches = Batch.objects.filter(students__in=[student], is_active=True)
        attendance_sheets = AttendanceSheet.objects.filter(
            assignment__batch__in=active_batches
        )
        from_date_str = request.query_params.get("from_date")
        to_date_str = request.query_params.get("to_date")
        last_days = request.query_params.get("last_days")
        last_month = request.query_params.get("last_month")

        today = timezone.now().date()

        if from_date_str and to_date_str:
            from_date = date.fromisoformat(from_date_str)
            to_date = date.fromisoformat(to_date_str)
            attendance_sheets = attendance_sheets.filter(
                date__range=(from_date, to_date)
            )
        elif last_days:
            last_days = int(last_days)
            start_date = today - timedelta(days=last_days)
            attendance_sheets = attendance_sheets.filter(
                date__range=(start_date, today)
            )
        elif last_month:
            start_date = today - timedelta(days=today.day)
            end_date = today.replace(day=1) - timedelta(days=1)
            attendance_sheets = attendance_sheets.filter(
                date__range=(start_date, end_date)
            )

        serializer = self.serializer_class(
            attendance_sheets, context={"user": user}, many=True
        )

        student_attendance_sheets = Attendance.objects.filter(
            student=student, attendancesheet__in=attendance_sheets
        )

        attendance_counts = student_attendance_sheets.aggregate(
            total_count=Count("id"),
            present_count=Count(Case(When(present=True, then=F("id")))),
        )

        absent_count = (
            attendance_counts["total_count"] - attendance_counts["present_count"]
        )

        course_counts = defaultdict(lambda: {"present": 0, "absent": 0})

        # Iterate through the attendance records
        for record in serializer.data:
            course_name = record["course_name"]
            present = record["attendance_records"][0]["present"]

            # Update counts for present and absent
            if present:
                course_counts[course_name]["present"] += 1
            else:
                course_counts[course_name]["absent"] += 1

        courses_attendance = [
            {
                "subject": course_name,
                **counts,
                "percent": (counts["present"])
                * 100
                / (counts["present"] + counts["absent"]),
            }
            for course_name, counts in course_counts.items()
        ]

        return Response(
            {
                "attendance_records": serializer.data,
                "present": attendance_counts["present_count"],
                "absent": absent_count,
                "total_classes": attendance_counts["total_count"],
                "total_attendance": attendance_counts["present_count"]
                / attendance_counts["total_count"]
                * 100,
                "course_wise": courses_attendance,
            },
            status=status.HTTP_200_OK,
        )

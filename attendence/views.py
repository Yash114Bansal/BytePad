from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.models import Batch, StudentModel
from accounts.permissions import IsFaculty, IsStudent

from .models import Attendance, AttendanceSheet
from .serializers import (
    AttendanceSheetSerializer,
    FacultyBatchAttendanceSerializer,
    StudentAttendanceResponseSerializer,
    AttendanceUpdateSerializer,
)


class AttendenceSheetCreateView(GenericAPIView):
    queryset = AttendanceSheet.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFaculty]
    serializer_class = AttendanceSheetSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "successfully created attendance sheet"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendenceSheetDeleteView(GenericAPIView):
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
        except Batch.DoesNotExist:
            return Response(
                {"message": "batch does not exists"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(attendance_sheets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AttendanceUpdateView(UpdateAPIView):
    queryset = Attendance.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFaculty]
    serializer_class = AttendanceUpdateSerializer


class StudentAttendanceView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudent]
    serializer_class = StudentAttendanceResponseSerializer

    def get(self, request):
        user = request.user
        student = StudentModel.objects.get(user=user)

        active_batches = Batch.objects.filter(students__in=[student], is_active=True)
        attendance_sheets = AttendanceSheet.objects.filter(
            assignment__batch__in=active_batches
        )

        serializer = self.serializer_class(
            attendance_sheets, context={"user": user}, many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

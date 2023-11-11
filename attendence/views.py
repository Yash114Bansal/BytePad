from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView,DestroyAPIView,CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.permissions import IsFaculty

from .models import Attendance, AttendanceSheet
from .serializers import AttendanceSerializer, AttendanceSheetSerializer


class AttendenceSheetCreateView(GenericAPIView):
    queryset = AttendanceSheet.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFaculty]
    serializer_class = AttendanceSheetSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"successfully created attendance sheet"},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class AttendenceSheetDeleteView(GenericAPIView):
    queryset = AttendanceSheet.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFaculty]

    def delete(self, request, pk):
        try:
            attendance_sheet = AttendanceSheet.objects.get(pk=pk)
        except AttendanceSheet.DoesNotExist:
            return Response({"message": "Attendance sheet not found"}, status=status.HTTP_404_NOT_FOUND)

        attendance_sheet.delete()
        return Response({"message": "Attendance sheet deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
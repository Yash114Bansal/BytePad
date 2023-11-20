from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import Batch, StudentModel
from accounts.permissions import IsHOD
from .models import LectureModel, TimeTableModel
from .serializers import LectureCreateSerializer, StudentLectureViewSerializer


class LectureCreateView(generics.CreateAPIView, generics.UpdateAPIView):
    """
    Create / Update Time Table (HOD only)

    API Endpoint To Add Lectures Of Time Table
    """
    queryset = LectureModel.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsHOD]
    serializer_class = LectureCreateSerializer

    def create(self, request, *args, **kwargs):
        batch_id = kwargs.get("batch_id")
        try:
            batch = Batch.objects.get(pk=batch_id)
        except Batch.DoesNotExist:
            return Response(
                {"detail": f"Batch with ID {batch_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lecture = serializer.save()

        # Assuming that LectureModel has a ForeignKey to BatchCourseFacultyAssignment called 'subject'
        timetable, created = TimeTableModel.objects.get_or_create(batch=batch)
        timetable.lectures.add(lecture)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        batch_id = kwargs.get("batch_id")
        lecture_id = kwargs.get("pk")
        try:
            batch = Batch.objects.get(pk=batch_id)
            lecture = LectureModel.objects.get(pk=lecture_id)
        except Batch.DoesNotExist:
            return Response(
                {"detail": f"Batch with ID {batch_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except LectureModel.DoesNotExist:
            return Response(
                {"detail": f"Lecture with ID {lecture_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(lecture, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

class TimeTableView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):

        user = request.user

        if user.is_student:
                
            student = StudentModel.objects.get(user=user)
            batch=Batch.objects.filter(is_active=True, students=student).first()
            timetable = TimeTableModel.objects.get(batch=batch)

            lectures = timetable.lectures.all()

            serializer = StudentLectureViewSerializer(lectures,many=True)

            return Response(serializer.data,status=status.HTTP_200_OK)

        return Response({})
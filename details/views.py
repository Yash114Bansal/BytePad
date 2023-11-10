from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from accounts.models import Batch
from accounts.permissions import IsFaculty
from django.db.models import Q
from .serializers import BatchDetailSerializer, StudentSerializer
from rest_framework.response import Response

class BatchDetailView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFaculty]

    def get(self, request):
        user_email = request.user.email

        active_batches_with_faculty = Batch.objects.filter(is_active=True).filter(
            Q(batchcoursefacultyassignment__faculty__email=user_email)
        )

        if active_batches_with_faculty:
            serializer = BatchDetailSerializer(active_batches_with_faculty, many=True)   
            return Response(serializer.data)
        
        else:
            return Response({'message': 'No active batches with faculty found.'}, status=404)

class StudentListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFaculty]

    def get(self, request, pk, *args, **kwargs):
        try:
            batch = Batch.objects.get(pk=pk)
        except Batch.DoesNotExist:
            return Response({"message": "Batch not found"}, status=404)

        batch_students = batch.students.all()
        serializer = StudentSerializer(batch_students,many=True)

        if serializer.is_valid():
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
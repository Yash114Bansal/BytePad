from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.models import Batch
from accounts.permissions import IsFaculty
from django.db.models import Q
from .serializers import BatchDetailSerializer
from rest_framework.response import Response


class BatchDetailView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFaculty]

    def get(self, request, *args, **kwargs):
        user_email = request.user.email

        active_batches_with_faculty = Batch.objects.filter(is_active=True).filter(
            Q(batchcoursefacultyassignment__faculty__email=user_email)
        )

        if active_batches_with_faculty:
            serializer = BatchDetailSerializer(active_batches_with_faculty, many=True)   
            return Response(serializer.data)
        
        else:
            return Response({'message': 'No active batches with faculty found.'}, status=404)

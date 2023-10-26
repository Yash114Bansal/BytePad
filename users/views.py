from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import UserSerializer, StudentSerializer, FacultySerializer
from accounts.models import UserProfile, StudentModel, FacultyModel


class UserDetailsView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            # Getting User With Corresponding ID
            user = UserProfile.objects.get(email=request.user.email)
            
            serializer = UserSerializer(user)
            
            additional_data = {}

            # If The User Is A Faculty, Include Faculty Details
            if user.is_faculty:
                faculty = FacultyModel.objects.get(email=user.email)
                faculty_serializer = FacultySerializer(faculty)
                additional_data = faculty_serializer.data

            # If The User Is A Student, Include Student Details
            if user.is_student:
                student = StudentModel.objects.get(email=user.email)
                student_serializer = StudentSerializer(student)
                additional_data = student_serializer.data

            # Merge The Additional Data Into The User Data
            response_data = {
                **serializer.data,
                **additional_data
            }

            # Return The Response With A Status Code Of 200
            return Response(response_data, status=status.HTTP_200_OK)

        # If User Profile Does Not Exists
        except UserProfile.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        # If User Is Faculty And Faculty Details Does Not Exists
        except FacultyModel.DoesNotExist:
            return Response({'message': 'Faculty data not found'}, status=status.HTTP_400_BAD_REQUEST)

        # If User Is Student And Student Details Does Not Exists
        except StudentModel.DoesNotExist:
            return Response({'message': 'Student data not found'}, status=status.HTTP_400_BAD_REQUEST)

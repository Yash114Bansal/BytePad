from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import UserSerializer, StudentSerializer, FacultySerializer
from accounts.models import UserProfile, StudentModel, FacultyModel


class UserDetailsView(GenericAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            # Get the user using the request.user.id
            user = UserProfile.objects.get(id=request.user.id)
            
            # Serialize the user data using the UserSerializer
            serializer = UserSerializer(user)

            # Initialize additional data as an empty dictionary
            additional_data = {}

            # If the user is a faculty, include faculty details
            if user.is_faculty:
                faculty = FacultyModel.objects.get(id=user.id)
                faculty_serializer = FacultySerializer(faculty)
                additional_data = faculty_serializer.data

            # If the user is a student, include student details
            if user.is_student:
                student = StudentModel.objects.get(id=user.id)
                student_serializer = StudentSerializer(student)
                additional_data = student_serializer.data

            # Merge the additional data into the user data
            response_data = {
                **serializer.data,
                **additional_data
            }
            response_data.pop("id")
            # Return the response with a status code of 200 OK
            return Response(response_data, status=status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        except FacultyModel.DoesNotExist:
            return Response({'message': 'Faculty data not found'}, status=status.HTTP_400_BAD_REQUEST)

        except StudentModel.DoesNotExist:
            return Response({'message': 'Student data not found'}, status=status.HTTP_400_BAD_REQUEST)

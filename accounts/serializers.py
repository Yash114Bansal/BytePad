from rest_framework import serializers
from .models import UserProfile, StudentModel, FacultyModel
from .utils import send_welcome_email

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "email",
            "name",
            "password",
            "is_department_head",
            "is_faculty",
            "is_student",
        ]

    password = serializers.CharField(write_only=True)
    is_department_head = serializers.BooleanField(required=True)
    is_faculty = serializers.BooleanField(required=True)
    is_student = serializers.BooleanField(required=True)

    def create(self, validated_data):
        user = UserProfile.objects.create(
            email=validated_data["email"],
            is_department_head=validated_data["is_department_head"],
            is_faculty=validated_data["is_faculty"],
            is_student=validated_data["is_student"],
            name = validated_data["name"],
        )
        password = validated_data["password"]
        user.set_password(password)
        user.save()

        print(f"user={user.name},email={user.email},password={password}")
        send_welcome_email(user=user.name,email=user.email,password=password)

        return user


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModel
        fields = [
            "email",
            "roll_number",
            "current_semester",
            "branch",
            "contact_number",
            "date_of_birth",
            "guardian_name",
            "guardian_contact_number",
        ]


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyModel
        fields = [
            "email",
            "contact_number",
            "date_of_birth",
            "courses",
            "department",
            "is_department_head",
        ]

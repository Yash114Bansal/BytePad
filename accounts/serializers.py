from rest_framework import serializers
from .models import UserProfile, StudentModel, FacultyModel


class UserSerializer(serializers.ModelSerializer):
    is_department_head = serializers.BooleanField(required=True)
    is_faculty = serializers.BooleanField(required=True)
    is_student = serializers.BooleanField(required=True)

    class Meta:
        model = UserProfile
        fields = [
            "email",
            "name",
            "is_department_head",
            "is_faculty",
            "is_student",
        ]

    def create(self, validated_data):
        user = UserProfile.objects.create(
            email=validated_data["email"],
            is_department_head=validated_data["is_department_head"],
            is_faculty=validated_data["is_faculty"],
            is_student=validated_data["is_student"],
            name=validated_data["name"],
        )

        return user


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModel
        fields = [
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
            "contact_number",
            "date_of_birth",
            "department",
        ]

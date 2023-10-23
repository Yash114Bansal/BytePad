from rest_framework import serializers
from .models import UserProfile, StudentModel, FacultyModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "email",
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
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModel
        fields = [
            "id",
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
            "id",
            "contact_number",
            "date_of_birth",
            "courses",
            "department",
            "is_department_head",
        ]

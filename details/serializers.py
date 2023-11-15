from rest_framework import serializers
from accounts.models import Batch, StudentModel, Semester, Branch, Course


class BatchDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ["id","name","year","semester","branch"]


class StudentSerializer(serializers.ModelSerializer):
    
    user_name = serializers.CharField(source='user.name', read_only=True)
    profile_pic = serializers.FileField(source="user.profile_picture")

    class Meta:
        model = StudentModel
        fields = ['user_name', 'roll_number','profile_pic']


class BranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = "__all__"


class SemeterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Semester
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = "__all__"
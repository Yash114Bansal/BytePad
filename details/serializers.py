from rest_framework import serializers
from accounts.models import Batch,StudentModel


class BatchDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ["id","name","year","semester","branch"]


class StudentSerializer(serializers.ModelSerializer):
    
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = StudentModel
        fields = ['user_name', 'roll_number']

from rest_framework import serializers
from accounts.models import Batch,StudentModel


class BatchDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ["id","name","year","semester","branch"]

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModel
        fields = ['roll_number']
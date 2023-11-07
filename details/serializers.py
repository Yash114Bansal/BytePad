from rest_framework import serializers
from accounts.models import Batch


class BatchDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ["id","name","year","semester","branch"]
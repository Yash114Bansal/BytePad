from rest_framework import serializers
from .models import SamplePaper,SamplePaperSolution

class SamplePaperSerializer(serializers.ModelSerializer):

    class Meta:
        model = SamplePaper
        fields = ['id','title', 'file', 'year', 'semester', 'courses']

class SolutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SamplePaperSolution
        fields = ['id','paper', 'file',]


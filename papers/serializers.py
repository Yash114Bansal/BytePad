from rest_framework import serializers
from .models import SamplePaper,SamplePaperSolution, MyCollections

class SamplePaperSerializer(serializers.ModelSerializer):

    class Meta:
        model = SamplePaper
        fields = ['id','title', 'file', 'year', 'semester', 'courses']

class SolutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SamplePaperSolution
        fields = ['id','paper', 'file',]

class MyCollectionsSerailizer(serializers.ModelSerializer):

    class Meta:
        model = MyCollections
        fields = ['id','paper']

class MyCollectionsGetSerailizer(serializers.ModelSerializer):
    
    title = serializers.CharField(source="paper.title")
    year = serializers.CharField(source="paper.year")
    semester = serializers.CharField(source="paper.semester")
    courses = serializers.StringRelatedField(many=True, source="paper.courses")

    class Meta:
        model = MyCollections
        fields = ['id','title','year','semester','courses','paper']


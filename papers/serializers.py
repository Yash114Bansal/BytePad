from rest_framework import serializers
from .models import SamplePaper, Course

class SamplePaperUploadSerializer(serializers.ModelSerializer):

    course_code = serializers.CharField(required=False)
    # id = serializers.SerializerMethodField()

    class Meta:
        model = SamplePaper
        fields = ['id','title', 'file', 'year', 'semester', 'course_code']

    # def get_id(self, obj):
    #     return obj.id

    def create(self, validated_data):
        course_code = validated_data.pop('course_code', None)

        if course_code:
            courses = Course.objects.filter(course_code=course_code)
        else:
            courses = []

        sample_paper = SamplePaper.objects.create(**validated_data)
        sample_paper.courses.add(*courses)

        return sample_paper

    def update(self, instance, validated_data):
        course_code = validated_data.pop('course_code', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if course_code:
            courses = Course.objects.filter(course_code=course_code)
            instance.courses.set(courses)
        else:
            instance.courses.clear()

        return instance

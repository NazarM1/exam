from rest_framework import serializers
from exam.models import Period4Exam

class Period4ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period4Exam
        fields = '__all__'

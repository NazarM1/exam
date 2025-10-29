from rest_framework import serializers
from exam.models import ExamRegistration

class ExamRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamRegistration
        fields = '__all__'

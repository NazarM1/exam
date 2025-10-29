from rest_framework import serializers
from exam.models import Invigilator

class InvigilatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invigilator
        fields = '__all__'

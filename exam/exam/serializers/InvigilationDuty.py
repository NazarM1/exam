from rest_framework import serializers
from exam.models.InvigilationDuty import InvigilationDuty

class InvigilationDutySerializer(serializers.ModelSerializer):
    class Meta:
        model = InvigilationDuty
        fields = '__all__'

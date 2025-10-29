from rest_framework import serializers
from exam.models import OutExamVenue

class OutExamVenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutExamVenue
        fields = '__all__'

from rest_framework import serializers
from exam.models.ExamVenue import ExamVenue

class ExamVenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamVenue
        fields = '__all__'

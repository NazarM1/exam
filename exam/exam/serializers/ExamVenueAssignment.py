from rest_framework import serializers
from exam.models import ExamVenueAssignment

class ExamVenueAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamVenueAssignment
        fields = '__all__'

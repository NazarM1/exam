from rest_framework import serializers
from exam.models.ExamVenueAssignment import ExamVenueAssignment

class ExamVenueAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamVenueAssignment
        fields = '__all__'

from rest_framework import serializers
from exam.models.ExamConflict import ExamConflict

class ExamConflictSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamConflict
        fields = '__all__'

from rest_framework import viewsets
from exam.models import ExamSchedule
from exam.serializers.ExamSchedule import ExamScheduleSerializer

class ExamScheduleViewSet(viewsets.ModelViewSet):
    queryset = ExamSchedule.objects.prefetch_related()
    serializer_class = ExamScheduleSerializer

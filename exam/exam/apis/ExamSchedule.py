from rest_framework import viewsets
from exam.serializers.ExamSchedule import ExamScheduleSerializer,ExamSchedule

class ExamScheduleViewSet(viewsets.ModelViewSet):
    queryset = ExamSchedule.objects.prefetch_related()
    serializer_class = ExamScheduleSerializer

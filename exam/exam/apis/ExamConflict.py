from rest_framework import viewsets
from exam.serializers.ExamConflict import ExamConflictSerializer,ExamConflict

class ExamConflictViewSet(viewsets.ModelViewSet):
    queryset = ExamConflict.objects.prefetch_related()
    serializer_class = ExamConflictSerializer

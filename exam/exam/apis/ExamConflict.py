from rest_framework import viewsets
from exam.models import ExamConflict
from exam.serializers.ExamConflict import ExamConflictSerializer

class ExamConflictViewSet(viewsets.ModelViewSet):
    queryset = ExamConflict.objects.prefetch_related()
    serializer_class = ExamConflictSerializer

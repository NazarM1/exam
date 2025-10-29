from rest_framework import viewsets
from exam.models import Period4Exam
from exam.serializers.Period4Exam import Period4ExamSerializer

class Period4ExamViewSet(viewsets.ModelViewSet):
    queryset = Period4Exam.objects.prefetch_related()
    serializer_class = Period4ExamSerializer

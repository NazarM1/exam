from rest_framework import viewsets
from exam.models import ExamRegistration
from exam.serializers.ExamRegistration import ExamRegistrationSerializer

class ExamRegistrationViewSet(viewsets.ModelViewSet):
    queryset = ExamRegistration.objects.prefetch_related()
    serializer_class = ExamRegistrationSerializer

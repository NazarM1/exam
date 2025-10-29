from rest_framework import viewsets
from exam.serializers.ExamRegistration import ExamRegistrationSerializer,ExamRegistration

class ExamRegistrationViewSet(viewsets.ModelViewSet):
    queryset = ExamRegistration.objects.prefetch_related()
    serializer_class = ExamRegistrationSerializer

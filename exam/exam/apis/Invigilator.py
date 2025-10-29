from rest_framework import viewsets
from exam.models import Invigilator
from exam.serializers.Invigilator import InvigilatorSerializer

class InvigilatorViewSet(viewsets.ModelViewSet):
    queryset = Invigilator.objects.prefetch_related()
    serializer_class = InvigilatorSerializer

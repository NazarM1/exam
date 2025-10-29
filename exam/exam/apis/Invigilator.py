from rest_framework import viewsets
from exam.serializers.Invigilator import InvigilatorSerializer, Invigilator

class InvigilatorViewSet(viewsets.ModelViewSet):
    queryset = Invigilator.objects.prefetch_related()
    serializer_class = InvigilatorSerializer

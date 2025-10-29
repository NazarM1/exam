from rest_framework import viewsets
from exam.models import InvigilationDuty
from exam.serializers.InvigilationDuty import InvigilationDutySerializer

class InvigilationDutyViewSet(viewsets.ModelViewSet):
    queryset = InvigilationDuty.objects.prefetch_related()
    serializer_class = InvigilationDutySerializer

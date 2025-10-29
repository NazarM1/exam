from rest_framework import viewsets
from exam.serializers.InvigilationDuty import InvigilationDutySerializer,InvigilationDuty

class InvigilationDutyViewSet(viewsets.ModelViewSet):
    queryset = InvigilationDuty.objects.prefetch_related()
    serializer_class = InvigilationDutySerializer

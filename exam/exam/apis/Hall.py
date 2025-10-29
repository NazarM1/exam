from rest_framework import viewsets
from exam.models import Hall
from exam.serializers.Hall import HallSerializer

class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.prefetch_related()
    serializer_class = HallSerializer

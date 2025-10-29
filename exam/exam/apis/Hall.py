from rest_framework import viewsets
from exam.serializers.Hall import HallSerializer,Hall

class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.prefetch_related()
    serializer_class = HallSerializer

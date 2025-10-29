from rest_framework import viewsets
from exam.models import UnavailableDate
from exam.serializers.UnavailableDate import UnavailableDateSerializer

class UnavailableDateViewSet(viewsets.ModelViewSet):
    queryset = UnavailableDate.objects.prefetch_related()
    serializer_class = UnavailableDateSerializer

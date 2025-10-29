from rest_framework import viewsets
from exam.serializers.UnavailableDate import UnavailableDateSerializer,UnavailableDate

class UnavailableDateViewSet(viewsets.ModelViewSet):
    queryset = UnavailableDate.objects.prefetch_related()
    serializer_class = UnavailableDateSerializer

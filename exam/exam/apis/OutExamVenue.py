from rest_framework import viewsets
from exam.models import OutExamVenue
from exam.serializers.OutExamVenue import OutExamVenueSerializer

class OutExamVenueViewSet(viewsets.ModelViewSet):
    queryset = OutExamVenue.objects.prefetch_related()
    serializer_class = OutExamVenueSerializer

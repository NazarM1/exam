from rest_framework import viewsets
from exam.serializers.OutExamVenue import OutExamVenueSerializer,OutExamVenue

class OutExamVenueViewSet(viewsets.ModelViewSet):
    queryset = OutExamVenue.objects.prefetch_related()
    serializer_class = OutExamVenueSerializer

from rest_framework import viewsets
from exam.serializers.ExamVenue import ExamVenueSerializer,ExamVenue

class ExamVenueViewSet(viewsets.ModelViewSet):
    queryset = ExamVenue.objects.prefetch_related()
    serializer_class = ExamVenueSerializer

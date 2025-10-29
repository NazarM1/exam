from rest_framework import viewsets
from exam.models import ExamVenue
from exam.serializers.ExamVenue import ExamVenueSerializer

class ExamVenueViewSet(viewsets.ModelViewSet):
    queryset = ExamVenue.objects.allprefetch_related()
    serializer_class = ExamVenueSerializer

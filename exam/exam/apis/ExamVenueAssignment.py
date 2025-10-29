from rest_framework import viewsets
from exam.models import ExamVenueAssignment
from exam.serializers.ExamVenueAssignment import ExamVenueAssignmentSerializer

class ExamVenueAssignmentViewSet(viewsets.ModelViewSet):
    queryset = ExamVenueAssignment.objects.prefetch_related()
    serializer_class = ExamVenueAssignmentSerializer

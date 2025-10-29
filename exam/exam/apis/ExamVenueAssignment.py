from rest_framework import viewsets
from exam.serializers.ExamVenueAssignment import ExamVenueAssignmentSerializer,ExamVenueAssignment

class ExamVenueAssignmentViewSet(viewsets.ModelViewSet):
    queryset = ExamVenueAssignment.objects.prefetch_related()
    serializer_class = ExamVenueAssignmentSerializer

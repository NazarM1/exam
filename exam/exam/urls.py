from django.urls import path, include
from rest_framework.routers import DefaultRouter

from exam.apis.Hall import HallViewSet
from exam.apis.OutExamVenue import OutExamVenueViewSet
from exam.apis.ExamVenue import ExamVenueViewSet
from exam.apis.Period4Exam import Period4ExamViewSet
from exam.apis.ExamSchedule import ExamScheduleViewSet
from exam.apis.ExamVenueAssignment import ExamVenueAssignmentViewSet
from exam.apis.ExamRegistration import ExamRegistrationViewSet
from exam.apis.Invigilator import InvigilatorViewSet
from exam.apis.UnavailableDate import UnavailableDateViewSet
from exam.apis.InvigilationDuty import InvigilationDutyViewSet
from exam.apis.ExamConflict import ExamConflictViewSet

router = DefaultRouter()
router.register(r'halls', HallViewSet)
router.register(r'out-venues', OutExamVenueViewSet)
router.register(r'exam-venues', ExamVenueViewSet)
router.register(r'periods', Period4ExamViewSet)
router.register(r'schedules', ExamScheduleViewSet)
router.register(r'venue-assignments', ExamVenueAssignmentViewSet)
router.register(r'exam-registrations', ExamRegistrationViewSet)
router.register(r'invigilators', InvigilatorViewSet)
router.register(r'unavailable-dates', UnavailableDateViewSet)
router.register(r'invigilation-duties', InvigilationDutyViewSet)
router.register(r'conflicts', ExamConflictViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

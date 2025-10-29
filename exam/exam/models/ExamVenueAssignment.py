from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from .ExamSchedule import ExamSchedule
from .ExamVenue import ExamVenue

from .base import SoftDeleteModel


class ExamVenueAssignment(SoftDeleteModel):
    fk_exam_schedule = models.ForeignKey(ExamSchedule, related_name='venue_assignments', on_delete=models.CASCADE, verbose_name=_('جدول الامتحان'))
    fk_exam_venue = models.ForeignKey(ExamVenue, related_name='assignments', on_delete=models.CASCADE, verbose_name=_('مكان الامتحان'))
    capacity_allocated = models.IntegerField(help_text=_('Number of seats allocated from this venue for this exam'), verbose_name=_('السعة المخصصة'))
    student_count = models.IntegerField(default=0, help_text=_('Number of students actually assigned to this venue'), verbose_name=_('عدد الطلاب'))

    class Meta:
        verbose_name = _('تخصيص قاعة للاختبار')
        verbose_name_plural = _('تخصيصات قاعات الامتحان')
        indexes = [models.Index(fields=['fk_exam_schedule']), models.Index(fields=['fk_exam_venue'])]
        constraints = [models.UniqueConstraint(fields=['fk_exam_schedule', 'fk_exam_venue'], name='unique_fk_exam_schedule_fk_exam_hall_no_deleted', condition=Q(is_deleted=False))]

    @property
    def available_seats(self):
        return max(self.capacity_allocated - (self.student_count or 0), 0)

    def can_accommodate_more_students(self):
        return (self.student_count or 0) < (self.capacity_allocated or 0)
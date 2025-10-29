from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .base import SoftDeleteModel
from exam.choices.choices import DutyRole, DutyStatus


class InvigilationDuty(SoftDeleteModel):
    fk_invigilator = models.ForeignKey('Invigilator', on_delete=models.CASCADE, related_name='duties', verbose_name=_('المراقب'))
    fk_exam_venue = models.ForeignKey('ExamVenue', on_delete=models.CASCADE, related_name='invigilation_duties', null=True, blank=True, verbose_name=_('مكان الامتحان'))

    duty_role = models.PositiveSmallIntegerField(choices=DutyRole.choices, default=DutyRole.ASSISTANT, verbose_name=_('دور المهمة'))
    status = models.PositiveSmallIntegerField(choices=DutyStatus.choices, default=DutyStatus.ASSIGNED, verbose_name=_('حالة المهمة'))

    fk_preiod = models.ForeignKey('Period4Exam', on_delete=models.PROTECT, related_name='duties', verbose_name=_('الفترة'))

    responsibilities = models.TextField(blank=True, help_text=_('مهام ومسؤوليات محددة'), verbose_name=_('المسؤوليات'))
    requires_special_training = models.BooleanField(default=False, verbose_name=_('يتطلب تدريب خاص'))

    reporting_time = models.TimeField(help_text=_('وقت الحضور'), verbose_name=_('وقت الحضور'))
    assigned_date = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإسناد'))
    attendance_marked = models.BooleanField(default=False, verbose_name=_('تم تسجيل الحضور'))
    attendance_time = models.DateTimeField(null=True, blank=True, verbose_name=_('وقت الحضور'))
    performance_notes = models.TextField(blank=True, verbose_name=_('ملاحظات الأداء'))

    class Meta:
        verbose_name = _('مهمة مراقبة')
        verbose_name_plural = _('مهام المراقبة')
        indexes = [models.Index(fields=['fk_invigilator', 'status']), models.Index(fields=['fk_exam_venue', 'status']), models.Index(fields=['fk_preiod'])]
        constraints = [models.UniqueConstraint(fields=['fk_invigilator', 'fk_exam_venue', 'fk_preiod'], name='unique_fk_invigilator_fk_exam_venue_fk_preiod_no_deleted', condition=Q(is_deleted=False))]

    def __str__(self):
        venue_info = f" at {self.fk_exam_venue}" if self.fk_exam_venue else ""
        return f"{self.fk_invigilator.employee_id} - {self.get_duty_role_display()} {venue_info} ({self.fk_preiod})"

    @property
    def duty_duration(self):
        if self.fk_preiod and self.fk_preiod.start_time and self.fk_preiod.end_time:
            start_dt = timezone.datetime.combine(timezone.now().date(), self.fk_preiod.start_time)
            end_dt = timezone.datetime.combine(timezone.now().date(), self.fk_preiod.end_time)
            duration = end_dt - start_dt
            return duration.total_seconds() / 3600
        return 0
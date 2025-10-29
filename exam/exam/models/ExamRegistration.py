from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .base import SoftDeleteModel
from exam.choices.choices import RegistrationStatus


class ExamRegistration(SoftDeleteModel):
    fk_student_subject = models.ForeignKey('StudentSubject', on_delete=models.CASCADE, related_name='exam_registrations', verbose_name=_('الطالب'))
    fk_grades_record = models.ForeignKey('GradesRecord', on_delete=models.CASCADE, related_name='exam_registrations', verbose_name=_('سجل الدرجات'), null=True, blank=True)
    fk_exam_schedule = models.ForeignKey('ExamSchedule', on_delete=models.CASCADE, related_name='registrations', verbose_name=_('جدول الامتحان'))
    fk_venue = models.ForeignKey('ExamVenue', on_delete=models.CASCADE, related_name='scheduled_registrations', verbose_name=_('مكان الامتحان'))
    fk_exam_form = models.ForeignKey('TestForm', on_delete=models.CASCADE, related_name='scheduled_registrations', verbose_name=_('نموذج الامتحان'), null=True, blank=True)

    registration_date = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ التسجيل'))
    status = models.PositiveSmallIntegerField(choices=RegistrationStatus.choices, default=RegistrationStatus.REGISTERED, verbose_name=_('حالة التسجيل'))

    seating_no = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('رقم الجلوس'))
    pin = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=_('الرقم السري'))

    grade = models.CharField(max_length=2, blank=True, verbose_name=_('الدرجة'))
    remarks = models.TextField(blank=True, verbose_name=_('ملاحظات'))

    class Meta:
        verbose_name = _('تسجيل امتحان')
        verbose_name_plural = _('تسجيلات الامتحانات')
        constraints = [models.UniqueConstraint(fields=['fk_student_subject', 'fk_exam_schedule'], name='unique_student_exam_no_deleted', condition=Q(is_deleted=False))]
        indexes = [models.Index(fields=['fk_student_subject', 'status']), models.Index(fields=['fk_exam_schedule', 'status'])]

    def __str__(self):
        return f"{self.fk_student_subject} - {self.fk_exam_schedule}"
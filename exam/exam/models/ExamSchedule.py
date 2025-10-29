from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from .base import SoftDeleteModel

from exam.choices.choices import ExamType, ExamStatus

class ExamSchedule(SoftDeleteModel):
    fk_semester_subject = models.ForeignKey('system_management.SemesterSubject', related_name='exam_schedules', on_delete=models.CASCADE, verbose_name=_('مادة الفصل'))
    fk_grade_distribution = models.ForeignKey('system_management.GradeDistribution', related_name='exam_schedules', on_delete=models.CASCADE, verbose_name=_('توزيع الدرجات'))
    exam_type = models.PositiveSmallIntegerField(choices=ExamType.choices, verbose_name=_('نوع الامتحان'))
    title = models.CharField(max_length=200, verbose_name=_('العنوان'))
    description = models.TextField(blank=True, verbose_name=_('الوصف'))

    exam_date = models.DateField(verbose_name=_('تاريخ الامتحان'))
    fk_preiod = models.ForeignKey('Period4Exam', on_delete=models.PROTECT, related_name='exam_schedules', verbose_name=_('الفترة'))

    status = models.PositiveSmallIntegerField(choices=ExamStatus.choices, default=ExamStatus.SCHEDULED, verbose_name=_('حالة الامتحان'))
    max_students = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True, verbose_name=_('الحد الأقصى للطلاب'))
    is_rescheduled = models.BooleanField(default=False, verbose_name=_('معاد جدولته'))
    original_schedule = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('الجدول الأصلي'))

    venues = models.ManyToManyField('ExamVenue', through='ExamVenueAssignment', related_name='exam_schedules', verbose_name=_('أماكن الامتحان'))

    class Meta:
        verbose_name = _('جدول الامتحان')
        verbose_name_plural = _('جداول الامتحانات')
        indexes = [models.Index(fields=['exam_date', 'fk_preiod']), models.Index(fields=['fk_semester_subject']), models.Index(fields=['exam_type', 'status'])]
        ordering = ['exam_date']

    def __str__(self):
        return f"{self.fk_semester_subject} - {self.get_exam_type_display()} - {self.exam_date}"

    @property
    def total_capacity(self):
        return sum(a.capacity_allocated for a in self.venue_assignments.all())

    @property
    def assigned_venues(self):
        return [a.fk_exam_venue for a in self.venue_assignments.all()]

    def get_day_name(self):
        return _(self.exam_date.strftime('%A'))

    def get_weekday(self):
        return self.exam_date.weekday()
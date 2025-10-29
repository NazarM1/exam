from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .base import SoftDeleteModel
from exam.choices.choices import DutyStatus


class Invigilator(SoftDeleteModel):
    fk_branch = models.ForeignKey('system_management.Organization', on_delete=models.PROTECT, verbose_name=_('الفرع'), null=True, blank=True)
    fk_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='invigilator_profile', verbose_name=_('المستخدم'))
    employee_id = models.PositiveIntegerField(verbose_name=_('رقم الموظف'), null=True, blank=True)
    phone_number = models.CharField(max_length=15, verbose_name=_('رقم الهاتف'))

    max_duties_per_day = models.IntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name=_('أقصى واجبات يومية'))
    max_duties_per_week = models.IntegerField(default=6, validators=[MinValueValidator(1), MaxValueValidator(20)], verbose_name=_('أقصى واجبات أسبوعية'))

    can_supervise_labs = models.BooleanField(default=False, verbose_name=_('إشراف مختبرات'))
    can_handle_special_needs = models.BooleanField(default=False, verbose_name=_('التعامل مع احتياجات خاصة'))

    notes = models.TextField(blank=True, verbose_name=_('ملاحظات'))

    class Meta:
        verbose_name = _('مراقب')
        verbose_name_plural = _('المراقبون')
        indexes = [models.Index(fields=['employee_id']), models.Index(fields=['fk_user'])]
        constraints = [
             models.UniqueConstraint(fields=['fk_user', 'fk_branch'], name='unique_user_branch_no_deleted', condition=Q(is_deleted=False)),
             models.UniqueConstraint(fields=['employee_id', 'fk_branch'], name='unique_employee_id_branch_no_deleted', condition=Q(is_deleted=False))
             ]
    def __str__(self):
        return f"{self.employee_id} - {self.fk_user.get_full_name()}"

    @property
    def current_duties_count(self):
        start_of_week = timezone.now().date() - timezone.timedelta(days=timezone.now().weekday())
        end_of_week = start_of_week + timezone.timedelta(days=6)
        return self.duties.filter(fk_exam_schedule__exam_date__range=[start_of_week, end_of_week], status__in=[DutyStatus.ASSIGNED, DutyStatus.CONFIRMED]).count()

    @property
    def is_available_today(self):
        today = timezone.now().date()
        return not self.unavailability.filter(date=today, is_approved=True).exists()

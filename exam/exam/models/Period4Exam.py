from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .base import SoftDeleteModel


class Period4Exam(SoftDeleteModel):
    fk_branch = models.ForeignKey('system_management.Organization', on_delete=models.PROTECT, verbose_name=_('الفرع'), null=True, blank=True)
    order_no = models.PositiveSmallIntegerField(verbose_name=_('رقم الترتيب'))
    start_time = models.TimeField(verbose_name=_('بداية الفترة'))
    end_time = models.TimeField(verbose_name=_('نهاية الفترة'))
    duration_minutes = models.IntegerField(help_text=_('المدة بالدقائق'))

    class Meta:
        verbose_name = _('فترة الامتحان')
        verbose_name_plural = _('فترات الامتحان')
        indexes = [models.Index(fields=['order_no', 'fk_branch'])]
        constraints = [models.UniqueConstraint(fields=['order_no', 'fk_branch'], name='unique_order_no_fk_branch_no_deleted', condition=Q(is_deleted=False))]

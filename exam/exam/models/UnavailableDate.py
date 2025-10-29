from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .base import SoftDeleteModel


class UnavailableDate(SoftDeleteModel):
    fk_invigilator = models.ForeignKey('Invigilator', on_delete=models.CASCADE, related_name='unavailability', verbose_name=_('المراقب'))
    date = models.DateField(verbose_name=_('التاريخ'))
    reason = models.CharField(max_length=20, choices=[('SICK_LEAVE', _('إجازة مرضية')), ('VACATION', _('إجازة')), ('CONFERENCE', _('مؤتمر')), ('PERSONAL', _('شخصي')), ('OTHER', _('أخرى'))], verbose_name=_('السبب'))
    is_approved = models.BooleanField(default=True, verbose_name=_('موافق عليه'))

    class Meta:
        verbose_name = _('تواريخ عدم التوفر')
        verbose_name_plural = _('تواريخ عدم توفر المراقبين')
        constraints = [models.UniqueConstraint(fields=['fk_invigilator', 'date'], name='unique_invigilator_date_no_deleted')]

    def __str__(self):
        return f"{self.fk_invigilator.employee_id} - {self.date} - {self.get_reason_display()}"
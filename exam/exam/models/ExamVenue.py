from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from .base import SoftDeleteModel


class ExamVenue(SoftDeleteModel):
    """مكان الامتحان — داخلي أو خارجي."""
    fk_hall = models.ForeignKey('Hall', on_delete=models.PROTECT, related_name='exam_venues', verbose_name=_('قاعة داخلية'), null=True, blank=True)
    fk_out_exam_venue = models.ForeignKey('OutExamVenue', on_delete=models.PROTECT, related_name='exam_venues_out', verbose_name=_('مكان خارجي'), null=True, blank=True)
    capacity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name=_('السعة'))
    is_outside = models.BooleanField(default=False, verbose_name=_('مكان خارجي'))
    is_active = models.BooleanField(default=True, verbose_name=_('تمكين العمل على مكان الامتحان'))

    def __str__(self):
        return f"{'خارجي' if self.is_outside else 'داخلي'} - {self.fk_out_exam_venue or self.fk_hall}"

    class Meta:
        verbose_name = _('مكان الامتحان')
        verbose_name_plural = _('أماكن الامتحان')
        indexes = [models.Index(fields=['fk_hall']), models.Index(fields=['fk_out_exam_venue']), models.Index(fields=['is_outside', 'is_active'])]
        constraints = [
            models.UniqueConstraint(fields=['fk_hall', 'is_outside'], name='unique_fk_hall_is_outside_no_deleted', condition=Q(is_deleted=False)),
            models.UniqueConstraint(fields=['fk_out_exam_venue', 'is_outside'], name='unique_fk_out_exam_venue_is_outside_no_deleted', condition=Q(is_deleted=False)),
        ]

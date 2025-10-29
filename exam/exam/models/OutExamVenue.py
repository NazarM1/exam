from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from .base import SoftDeleteModel
from exam.choices.choices import VenueType


class OutExamVenue(SoftDeleteModel):
    fk_branch = models.ForeignKey('Organization', on_delete=models.PROTECT, verbose_name=_('الفرع'), null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name=_('الاسم'))
    code = models.CharField(max_length=20,verbose_name=_('الرمز'))
    venue_type = models.PositiveSmallIntegerField(choices=VenueType.choices, verbose_name=_('نوع المكان'))
    capacity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name=_('السعة'))
    building = models.CharField(max_length=100, verbose_name=_('المبنى'))
    floor = models.IntegerField(default=1, verbose_name=_('الطابق'))
    has_projector = models.BooleanField(default=False, verbose_name=_('جهاز عرض'))
    has_air_conditioning = models.BooleanField(default=False, verbose_name=_('تكييف'))
    is_available = models.BooleanField(default=True, verbose_name=_('متاح'))

    class Meta:
        verbose_name = _('مكان اختبارات خارجي')
        verbose_name_plural = _('أماكن اختبارات خارجية')
        indexes = [models.Index(fields=['code']), models.Index(fields=['building', 'fk_branch'])]
        constraints = [models.UniqueConstraint(fields=['code', 'building', 'fk_branch'], name='unique_code_building_no_deleted', condition=Q(is_deleted=False))]

    def __str__(self):
        return f"{self.code} - {self.name} ({_('السعة')}: {self.capacity})"

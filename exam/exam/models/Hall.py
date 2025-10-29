from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from .base import SoftDeleteModel
from exam.choices.choices import VenueType


class Hall(SoftDeleteModel):
    fk_building = models.ForeignKey('system_management.Building', related_name='halls', on_delete=models.CASCADE, verbose_name=_('المبنى'))
    floor = models.CharField(max_length=30, verbose_name=_('الطابق'), null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name=_('الاسم'))
    code = models.CharField(max_length=20, verbose_name=_('الرمز'))
    venue_type = models.PositiveSmallIntegerField(choices=VenueType.choices, verbose_name=_('نوع المكان'))
    capacity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name=_('السعة'))
    has_projector = models.BooleanField(default=False, verbose_name=_('جهاز عرض'))
    has_air_conditioning = models.BooleanField(default=False, verbose_name=_('تكييف'))
    is_available = models.BooleanField(default=True, verbose_name=_('تمكين العمل على القاعة'))

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = _('قاعة')
        verbose_name_plural = _('القاعات')
        indexes = [models.Index(fields=['code']), models.Index(fields=['fk_building'])]
        constraints = [models.UniqueConstraint(fields=['code', 'fk_building'], name='unique_code_fk_building_no_deleted', condition=Q(is_deleted=False))]

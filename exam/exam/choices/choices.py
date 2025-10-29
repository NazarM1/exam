from django.db import models
from django.utils.translation import gettext_lazy as _

class VenueTypeChoices(models.IntegerChoices):
    CLASSROOM = 1, _('قاعة دراسية')
    HALL = 2, _('قاعة امتحانات')
    LAB = 3, _('مختبر')
    AUDITORIUM = 4, _('مدرج')

class ExamTypeChoices(models.IntegerChoices):
    MIDTERM = 1, _('اختبار منتصف الفصل')
    FINAL = 2, _('الاختبار النهائي')
    QUIZ = 3, _('اختبار قصير')
    PRACTICAL = 4, _('امتحان عملي')

class ExamStatusChoices(models.IntegerChoices):
    SCHEDULED = 1, _('مجدول')
    ONGOING = 2, _('قائم')
    COMPLETED = 3, _('مكتمل')
    CANCELLED = 4, _('ملغى')
    POSTPONED = 5, _('مؤجل')

class RegistrationStatusChoices(models.IntegerChoices):
    REGISTERED = 1, _('مسجل')
    CONFIRMED = 2, _('مؤكد')
    CANCELLED = 3, _('ملغى')
    ABSENT = 4, _('غائب')
    PASSED = 5, _('ناجح')
    FAILED = 6, _('راسب')

class DutyRoleChoices(models.IntegerChoices):
    CHIEF = 1, _('المشرف الرئيسي')
    DEPUTY_CHIEF = 2, _('نائب المشرف الرئيسي')
    SENIOR = 3, _('مراقب أول')
    ASSISTANT = 4, _('مراقب مساعد')
    FLOOR_INCHARGE = 5, _('مشرف الطابق')
    RESERVE = 6, _('مراقب احتياطي')

class DutyStatusChoices(models.IntegerChoices):
    ASSIGNED = 1, _('مكلف')
    CONFIRMED = 2, _('مؤكد')
    REJECTED = 3, _('مرفوض')
    COMPLETED = 4, _('مكتمل')
    CANCELLED = 5, _('ملغى')
    REPLACED = 6, _('مستبدل')

class ConflictTypeChoices(models.IntegerChoices):
    VENUE_OVERLAP = 1, _('تداخل قاعات')
    INVIGILATOR_OVERLAP = 2, _('تداخل مراقب')
    STUDENT_OVERLAP = 3, _('تداخل طالب')
    RESOURCE_CONFLICT = 4, _('تعارض مورد')

class ConflictStatusChoices(models.IntegerChoices):
    DETECTED = 1, _('مكتشف')
    RESOLVED = 2, _('مُحل')
    IGNORED = 3, _('متجاهل')

# Aliases to match names used in models
VenueType = VenueTypeChoices
ExamType = ExamTypeChoices
ExamStatus = ExamStatusChoices
RegistrationStatus = RegistrationStatusChoices
DutyRole = DutyRoleChoices
DutyStatus = DutyStatusChoices
ConflictType = ConflictTypeChoices
ConflictStatus = ConflictStatusChoices
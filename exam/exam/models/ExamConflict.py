
class ExamConflict(SoftDeleteModel):
    """نموذج لتسجيل حالات التعارض التي يكتشفها النظام أو المستخدم.

    سيناريوهات الشاشة:
      - عرض التعارضات المكتشفة تلقائياً (تداخل قاعات، تداخل مراقب، تداخل طلاب).
      - تمكين المشرف من تتبع وتوثيق الحلول (resolve) أو تجاهل تعارض معين.
      - ربط كل تعارض بجدولين (exam schedules) للمقارنة وعرض تفاصيل التداخل.

    
    """

    conflict_type = models.PositiveSmallIntegerField(choices=ConflictType.choices, verbose_name=_('نوع التعارض'))
    fk_exam_schedule_1 = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE, related_name='conflicts_as_first', verbose_name=_('الجدول الأول'))
    fk_exam_schedule_2 = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE, related_name='conflicts_as_second', verbose_name=_('الجدول الثاني'))
    detected_at = models.DateTimeField(auto_now_add=True, verbose_name=_('وقت الاكتشاف'))
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name=_('وقت الحل'))
    status = models.PositiveSmallIntegerField(choices=ConflictStatus.choices, default=ConflictStatus.DETECTED, verbose_name=_('حالة التعارض'))
    resolution_notes = models.TextField(blank=True, verbose_name=_('ملاحظات الحل'))

    class Meta:
        verbose_name = _('تعارض امتحان')
        verbose_name_plural = _('تعارضات الامتحانات')
        indexes = [
            models.Index(fields=['conflict_type']),
            models.Index(fields=['status']),
            models.Index(fields=['fk_exam_schedule_1']),
            models.Index(fields=['fk_exam_schedule_2']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['conflict_type', 'fk_exam_schedule_1', 'fk_exam_schedule_2'], name='unique_conflict_between_schedules_no_deleted', condition=Q(is_deleted=False))
        ]

    def __str__(self):
        return f"{self.get_conflict_type_display()} - {self.fk_exam_schedule_1} vs {self.fk_exam_schedule_2}"

    @property
    def involved_schedules(self):
        """Return the two involved ExamSchedule instances as a tuple."""
        return (self.fk_exam_schedule_1, self.fk_exam_schedule_2)
from rest_framework import serializers
from django.db import transaction
from django.db.models import Q

from exam.models.ExamSchedule import ExamSchedule
from ..models.ExamVenueAssignment import ExamVenueAssignment
from exam.serializers.ExamVenueAssignment import ExamVenueAssignmentSerializer

class ExamScheduleSerializer(serializers.ModelSerializer):
    venue_assignments = ExamVenueAssignmentSerializer(many=True, write_only=True, required=False)

    total_capacity = serializers.IntegerField(read_only=True)

    class Meta:
        model = ExamSchedule
        fields = '__all__'
        extra_fields = ['venue_assignments', 'total_capacity']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # expose computed fields and related assignments in read
        data['total_capacity'] = instance.total_capacity
        data['assigned_venues'] = [va.fk_exam_venue_id for va in instance.venue_assignments.all()]
        return data

    def validate(self, attrs):
        fk_semester_subject = attrs.get('fk_semester_subject') or getattr(self.instance, 'fk_semester_subject', None)
        exam_date = attrs.get('exam_date') or getattr(self.instance, 'exam_date', None)
        fk_preiod = attrs.get('fk_preiod') or getattr(self.instance, 'fk_preiod', None)
        max_students = attrs.get('max_students') if 'max_students' in attrs else getattr(self.instance, 'max_students', None)

        if not (fk_semester_subject and exam_date and fk_preiod):
            return attrs

        qs = ExamSchedule.objects.filter(
            fk_semester_subject=fk_semester_subject,
            exam_date=exam_date,
            fk_preiod=fk_preiod,
            is_deleted=False,
        )
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({'non_field_errors': ['لا يمكن تكرار نفس المادة في نفس الفترة والتاريخ.']})

        # Validate venue availability and capacity if venue_assignments provided
        request_data = self.initial_data if isinstance(self.initial_data, dict) else {}
        venue_assignments = request_data.get('venue_assignments')
        if venue_assignments:
            # check double-booking for each proposed venue
            venue_ids = [va.get('fk_exam_venue') or va.get('fk_exam_venue_id') for va in venue_assignments]
            venue_ids = [v for v in venue_ids if v]
            if venue_ids:
                conflict_assignments = ExamVenueAssignment.objects.filter(
                    fk_exam_venue_id__in=venue_ids,
                    fk_exam_schedule__exam_date=exam_date,
                    fk_exam_schedule__fk_preiod=fk_preiod,
                    fk_exam_schedule__is_deleted=False,
                    is_deleted=False,
                )
                if self.instance:
                    conflict_assignments = conflict_assignments.exclude(fk_exam_schedule=self.instance)
                if conflict_assignments.exists():
                    raise serializers.ValidationError({'venue_assignments': ['بعض القاعات محجوزة لنفس الفترة والتاريخ.']})

            # capacity check
            total_capacity = 0
            for va in venue_assignments:
                try:
                    cap = int(va.get('capacity_allocated') or 0)
                except (TypeError, ValueError):
                    cap = 0
                total_capacity += max(cap, 0)
            if max_students and total_capacity < max_students:
                raise serializers.ValidationError({'venue_assignments': ['إجمالي السعة المخصصة أقل من الحد الأقصى للطلاب.']})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        venue_assignments = self.initial_data.get('venue_assignments') if isinstance(self.initial_data, dict) else None
        schedule = ExamSchedule.objects.create(**validated_data)

        if venue_assignments:
            self._create_or_update_assignments(schedule, venue_assignments)

        return schedule

    @transaction.atomic
    def update(self, instance, validated_data):
        venue_assignments = self.initial_data.get('venue_assignments') if isinstance(self.initial_data, dict) else None
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if venue_assignments is not None:
            # simple strategy: delete existing (soft delete) and recreate
            instance.venue_assignments.filter(is_deleted=False).update(is_deleted=True)
            self._create_or_update_assignments(instance, venue_assignments)

        return instance

    def _create_or_update_assignments(self, schedule, assignments_data):
        serializer = ExamVenueAssignmentSerializer(data=assignments_data, many=True)
        serializer.is_valid(raise_exception=True)
        objs = []
        for item in serializer.validated_data:
            objs.append(ExamVenueAssignment(
                fk_exam_schedule=schedule,
                fk_exam_venue=item['fk_exam_venue'],
                capacity_allocated=item['capacity_allocated'],
                student_count=item.get('student_count', 0) or 0,
            ))
        if objs:
            ExamVenueAssignment.objects.bulk_create(objs)

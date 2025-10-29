from django.db import models

class Building(models.Model):
    name = models.CharField(max_length=100)

class Organization(models.Model):
    name = models.CharField(max_length=100)

class SemesterSubject(models.Model):
    title = models.CharField(max_length=200)

class GradeDistribution(models.Model):
    name = models.CharField(max_length=100)

class StudentSubject(models.Model):
    student_name = models.CharField(max_length=100)

class GradesRecord(models.Model):
    notes = models.TextField(blank=True)

class TestForm(models.Model):
    title = models.CharField(max_length=200)

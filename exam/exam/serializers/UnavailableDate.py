from rest_framework import serializers
from exam.models import UnavailableDate

class UnavailableDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnavailableDate
        fields = '__all__'

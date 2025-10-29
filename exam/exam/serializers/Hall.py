from rest_framework import serializers
from exam.models import Hall

class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'

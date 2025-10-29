from rest_framework import serializers
from exam.models.Hall import Hall

class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'

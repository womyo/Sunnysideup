from rest_framework import serializers
from .models import Rise, Set

class RiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rise
        fields = ('name', 'latitude', 'longitude', 'standard_time')

class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ('name', 'latitude', 'longitude', 'standard_time')
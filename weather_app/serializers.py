from rest_framework import serializers
from .models import Location, WeatherRecord

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class WeatherRecordSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = WeatherRecord
        fields = '__all__'

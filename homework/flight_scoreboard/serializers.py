from rest_framework import serializers
from .models import Flight, City, Status, TypeAirPlane


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = '__all__'


class TypeAirPlaneSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeAirPlane
        fields = '__all__'


class FlightSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)
    arrival_city = CitySerializer(read_only=True)
    dispatch_city = CitySerializer(read_only=True)
    type_airplane = TypeAirPlaneSerializer(read_only=True)

    class Meta:
        model = Flight
        fields = '__all__'
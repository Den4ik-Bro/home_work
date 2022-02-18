#-*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Flight, City, Status, TypeAirPlane
#
#
# class CitySerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = City
#         fields = '__all__'
#
#
# class StatusSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Status
#         fields = '__all__'
#
#
# class TypeAirPlaneSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = TypeAirPlane
#         fields = '__all__'


class FlightSerializer(serializers.ModelSerializer):
    status = serializers.StringRelatedField()
    arrival_city = serializers.StringRelatedField()
    dispatch_city = serializers.StringRelatedField()
    type_airplane = serializers.StringRelatedField()

    class Meta:
        model = Flight
        fields = '__all__'
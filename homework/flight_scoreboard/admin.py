#-*- coding: utf-8 -*-
from django.contrib import admin
from . import models


class FlightAdmin(admin.ModelAdmin):
    search_field = ('Status__title', 'City__name')
    # list_filter = ('arrival_city', 'status',)
    # list_display = ('number', 'arrival_city', 'status',)


admin.site.register(models.Flight, FlightAdmin)
admin.site.register(models.City)
admin.site.register(models.Status)
admin.site.register(models.TypeAirPlane)
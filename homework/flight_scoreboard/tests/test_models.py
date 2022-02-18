# coding=utf-8
from django.test import TestCase

# from flight_scoreboard.models import *

from ..models import *


class FlightModelTestCase(TestCase):

    def setUp(self):
        status = Status.objects.create(title='ok')
        type_airplane = TypeAirPlane.objects.create(title='самолет')
        arrival_city = City.objects.create(name='париж')
        dispatch_city = City.objects.create(name='москва')
        self.flight = Flight.objects.create(
            number='rt5656',
            type_airplane=type_airplane,
            arrival_city=arrival_city,
            dispatch_city=dispatch_city,
            status=status,
            departure_time='2022-02-22 15:00:00',
            arrival_time='2022-02-22 19:00:00',
        )

    def test_flight_number_label(self):
        flight = Flight.objects.get(id=1)
        field_label = flight._meta.get_field('number').verbose_name
        self.assertEqual(field_label, 'номер самолета')
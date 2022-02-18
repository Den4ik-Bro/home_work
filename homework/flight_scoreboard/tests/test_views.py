# coding=utf-8
from django.core.urlresolvers import reverse
from django.test import TestCase

from ..models import *


class FlightListTestCase(TestCase):

    def setUp(self):
        flights_list = 20
        status = Status.objects.create(title='ok')
        type_airplane = TypeAirPlane.objects.create(title='самолет')
        arrival_city = City.objects.create(name='париж')
        dispatch_city = City.objects.create(name='москва')
        for flight in range(flights_list):
            Flight.objects.create(
                number='qw12' + str(flight),
                type_airplane=type_airplane,
                arrival_city=arrival_city,
                dispatch_city=dispatch_city,
                departure_time=datetime.datetime('2022-02-22 15:00:00'),
                arrival_time=datetime.datetime('2022-02-22 19:00:00'),
            )

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('flight_scoreboard:home'))
        self.assertEqual(resp.status_code, 200)
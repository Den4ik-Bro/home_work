# coding=utf-8
import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import Client

from ..forms import SearchForm, CreateFlightForm
from ..models import *


class FlightListTestCase(TestCase):

    def setUp(self):
        flight_number = [
            'qw', 'wq', 'we', 'as', 'sa', 'sd', 'ds', 'df', 'fd', 'fg', 'gf', 'ww', 'ee', 'qq', 'rr', 'pl'
        ]
        status = Status.objects.create(title='ok')
        type_airplane = TypeAirPlane.objects.create(title='ИЛ-86')
        arrival_city = City.objects.create(name='париж')
        dispatch_city = City.objects.create(name='москва')
        for i in range(len(flight_number)):
            Flight.objects.create(
                number=flight_number[i] + '1234',
                type_airplane=type_airplane,
                status=status,
                arrival_city=arrival_city,
                dispatch_city=dispatch_city,
                departure_time=datetime.datetime.strptime('2022-02-25 15:00', '%Y-%m-%d %H:%M'),
                arrival_time=datetime.datetime.strptime('2022-02-26 19:00', '%Y-%m-%d %H:%M'),
            )
        test_user = User.objects.create_user(username='test_user', password='12345')
        test_user.save()

    def test_flight_list(self):
        server_response = self.client.get(reverse('flight_scoreboard:flight_list'))
        self.assertEqual(server_response.status_code, 200)
        self.assertTemplateUsed('flight_scoreboard/flight_list.html')

    def test_flight_detail_if_loggin(self):
        instance = Flight.objects.get(pk=1)
        self.client.login(username='test_user', password='12345')
        server_response = self.client.get(reverse('flight_scoreboard:current_flight', kwargs={'pk': instance.id}))
        self.assertEqual(server_response.status_code, 200)

    def test_flight_detail_if_not_loggin(self):
        instance = Flight.objects.get(pk=1)
        server_response = self.client.get(reverse('flight_scoreboard:current_flight', kwargs={'pk': instance.id}))
        self.assertEqual(server_response.status_code, 302)

    def test_get_absolute_url_flights(self):
        instance = Flight.objects.get(pk=1)
        self.assertEqual(instance.get_absolute_url(), '/detail_flight/1/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='test_user', password='12345')
        server_response = self.client.get(reverse('flight_scoreboard:flight_list'))
        self.assertEqual(str(server_response.context['user']), 'test_user')
        self.assertEqual(server_response.status_code, 200)

    def test_pagination_flight_list_view(self):
        server_response = self.client.get(reverse('flight_scoreboard:flight_list'))
        self.assertTrue(server_response.context['is_paginated'] == True)
        self.assertEqual(len(server_response.context['flights']), 5)
        server_response_page = self.client.get(reverse('flight_scoreboard:flight_list') + '?page=4')
        self.assertEqual(len(server_response_page.context['flights']), 1)

    def test_create_flight(self):
        user = Client()
        response = user.post('/admin/login/', {'username': 'test_user', 'password': '12345'})
        self.assertEqual(response.status_code, 200)
        data = {
            'number': 'cd1234',
            'type_airplane': 'test',
            'status': 'test',
            'arrival_city': 'testcity',
            'dispatch_city': 'testcity2',
            'departure_time': datetime.datetime.strptime('2022-02-25 15:00', '%Y-%m-%d %H:%M'),
            'arrival_time': datetime.datetime.strptime('2022-02-26 19:00', '%Y-%m-%d %H:%M'),
        }
        form = CreateFlightForm(data=data)
        user.post(reverse('flight_scoreboard:create_flight'), form)
        # self.client.post(reverse('flight_scoreboard:create_flight'), form)
        # instance = Flight.objects.get(number='cd1234')
        # self.assertEqual(instance.number, 'cd1234')
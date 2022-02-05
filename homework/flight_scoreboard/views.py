from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from rest_framework import viewsets, generics
from rest_framework.views import APIView

from .serializers import FlightSerializer, CitySerializer, StatusSerializer, TypeAirPlaneSerializer
from models import *
from forms import CreateFlightForm


def home(request):
    search_query = request.GET.get('q', '')
    if search_query:
        flights = Flight.objects.filter(
            Q(arrival_city__name__icontains=search_query) |
            Q(dispatch_city__name__icontains=search_query) |
            Q(status__title__icontains=search_query))
        return render(request, 'flight_scoreboard/home.html', {'flights': flights})
    else:
        flights = Flight.objects.all()
    if request.method == 'POST':
        form = CreateFlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('flight_scoreboard:home'))
    return render(request, 'flight_scoreboard/home.html', {'flights': flights})


def create_flight(request):
    form = CreateFlightForm()
    if request.method == 'POST':
        form = CreateFlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('flight_scoreboard:home'))
    return render(request, 'flight_scoreboard/create_flight.html', {'form':form})


def detail_flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    context = {
        'flight': flight
    }
    return render(request, 'flight_scoreboard/detail_flight.html', context)


def edit_flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    form = CreateFlightForm(instance=flight)
    if request.method == 'POST':
        form = CreateFlightForm(request.POST, instance=flight)
        if form.is_valid():
            form.save()
            return redirect(reverse('flight_scoreboard:current_flight', kwargs={'flight_id': flight.id}))
    return render(request, 'flight_scoreboard/edit_flight.html', {'form': form})


def delete_flight(request, flight_id):
    Flight.objects.get(pk=flight_id).delete()
    return redirect(reverse('flight_scoreboard:home'))


# API


class FlightsApiViewSet(viewsets.ModelViewSet):
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()


class CityApiViewSet(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()


class StatusApiViewSet(viewsets.ModelViewSet):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()


class TypeAirPlaneApiViewSet(viewsets.ModelViewSet):
    serializer_class = TypeAirPlaneSerializer
    queryset = TypeAirPlane.objects.all()
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from rest_framework import viewsets
from rest_framework.views import APIView

from .serializers import FlightSerializer, CitySerializer, StatusSerializer, TypeAirPlaneSerializer
from models import *
from forms import CreateFlightForm, SearchForm


class Home(ListView):
    queryset = Flight.objects.filter(
        Q(arrival_time__gte=(datetime.datetime.now())) |
        Q(departure_time__gte=(datetime.datetime.now()))
    )
    model = Flight
    template_name = 'flight_scoreboard/home.html'
    context_object_name = 'flights'
    paginate_by = 5
    form_class = SearchForm

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return super(Home, self).get_queryset().filter(
                Q(arrival_city__name__icontains=form.cleaned_data['q']) |
                Q(dispatch_city__name__icontains=form.cleaned_data['q']) |
                Q(status__title__icontains=form.cleaned_data['q'])
            )
        return super(Home, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        form = SearchForm()
        context['form'] = form
        return context


class CreateFlightView(CreateView):
    model = Flight
    template_name = 'flight_scoreboard/create_flight.html'
    form_class = CreateFlightForm
    success_url = '/'


class DetailFlightView(DetailView):
    model = Flight
    template_name = 'flight_scoreboard/detail_flight.html'
    context_object_name = 'flight'


class DeleteFlightsView(DeleteView):
    model = Flight
    template_name = 'flight_scoreboard/detail_flight.html'
    success_url = '/'

    def get(self, request, pk):
        return self.post(request, pk)


class UpdateFlightView(UpdateView):
    model = Flight
    template_name = 'flight_scoreboard/edit_flight.html'
    form_class = CreateFlightForm
    # success_url = '/'

    def get_success_url(self):
        flight = self.get_object()
        return redirect(reverse('flight_scoreboard:current_flight', kwargs={'pk': flight.id}))


# def home(request):
#     search_query = request.GET.get('q', '')
#     if search_query:
#         flights = Flight.objects.filter(
#             Q(arrival_city__name__icontains=search_query) |
#             Q(dispatch_city__name__icontains=search_query) |
#             Q(status__title__icontains=search_query))
#         return render(request, 'flight_scoreboard/home.html', {'flights': flights})
#     flights = Flight.objects.all()
#     return render(request, 'flight_scoreboard/home.html', {'flights': flights})


# def create_flight(request):
#     form = CreateFlightForm()
#     if request.method == 'POST':
#         form = CreateFlightForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('flight_scoreboard:home'))
#     return render(request, 'flight_scoreboard/create_flight.html', {'form':form})


# def detail_flight(request, flight_id):
#     flight = Flight.objects.get_or_404(pk=flight_id)
#     context = {
#         'flight': flight
#     }
#     return render(request, 'flight_scoreboard/detail_flight.html', context)


# def edit_flight(request, flight_id):
#     flight = Flight.objects.get(pk=flight_id)
#     if request.method == 'POST':
#         form = CreateFlightForm(request.POST, instance=flight)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('flight_scoreboard:current_flight', kwargs={'flight_id': flight.id}))
#     form = CreateFlightForm(instance=flight)
#     return render(request, 'flight_scoreboard/edit_flight.html', {'form': form})


# def delete_flight(request, flight_id):
#     Flight.objects.get(pk=flight_id).delete()
#     return redirect(reverse('flight_scoreboard:home'))


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
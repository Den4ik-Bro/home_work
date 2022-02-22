#-*- coding: utf-8 -*-
import django_filters.rest_framework
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from rest_framework.generics import ListAPIView
from rest_framework import filters
from .serializers import FlightSerializer
from models import *
from forms import CreateFlightForm, SearchForm


class Home(ListView):
    queryset = Flight.objects.filter(
        Q(arrival_time__gte=(datetime.datetime.now())) |
        Q(departure_time__gte=(datetime.datetime.now()))
    )
    template_name = 'flight_scoreboard/home.html'
    context_object_name = 'flights'
    paginate_by = 5
    form_class = SearchForm

    def get(self, request):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if 'q' in self.request.GET:
            form = self.form_class(self.request.GET)
            if form.is_valid():
                context[self.context_object_name] = self.get_queryset().filter(
                    Q(arrival_city__name__icontains=form.cleaned_data['q']) |
                    Q(dispatch_city__name__icontains=form.cleaned_data['q']) |
                    Q(status__title__icontains=form.cleaned_data['q'])
                )
            else:
                context['form'] = form
        return self.render_to_response(context)

    def get_queryset(self):
        return super(Home, self).get_queryset().select_related(
                'type_airplane',
                'arrival_city',
                'dispatch_city',
                'status',
            )

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        form = self.form_class()
        context['form'] = form
        context['q'] = self.request.GET.get('q')
        return context


class CreateFlightView(LoginRequiredMixin, CreateView):
    model = Flight
    template_name = 'flight_scoreboard/create_flight.html'
    form_class = CreateFlightForm
    success_url = '/'


class DetailFlightView(LoginRequiredMixin, DetailView):
    model = Flight
    template_name = 'flight_scoreboard/detail_flight.html'
    context_object_name = 'flight'


class DeleteFlightsView(LoginRequiredMixin, DeleteView):
    model = Flight
    template_name = 'flight_scoreboard/detail_flight.html'
    success_url = '/'

    def get(self, request, pk):
        return self.post(request, pk)


class UpdateFlightView(LoginRequiredMixin, UpdateView):
    model = Flight
    template_name = 'flight_scoreboard/edit_flight.html'
    form_class = CreateFlightForm

    # def get_success_url(self):
    #     flight = self.get_object()
    #     return redirect(reverse('flight_scoreboard:current_flight'))


# API


class GetAllFlight(ListAPIView):
    """пагинация определена через глобальные настройки"""
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter)
    search_fields = (
        'status__title',
        'arrival_city__name',
        'dispatch_city__name',
    )

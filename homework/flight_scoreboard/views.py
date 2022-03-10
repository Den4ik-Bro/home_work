#-*- coding: utf-8 -*-
import django_filters.rest_framework
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from rest_framework.generics import ListAPIView
from rest_framework import filters
from .serializers import FlightSerializer
from models import *
from forms import CreateFlightForm, SearchForm
import logging


logger = logging.getLogger('homework.flight_scoreboard.views')


class FlightListView(ListView):
    queryset = Flight.objects.filter(
        Q(arrival_time__gte=(datetime.datetime.now())) |
        Q(departure_time__gte=(datetime.datetime.now()))
    )
    template_name = 'flight_scoreboard/flight_list.html'
    context_object_name = 'flights'
    paginate_by = 5
    form_class = SearchForm

    def get(self, request):
        logger.debug('запрос страницы {0} на получение рейсов без параметров'
                     .format(request.GET.get(self.page_kwarg, 1)))
        return super(FlightListView, self).get(request)

    def get_queryset(self):
        return super(FlightListView, self).get_queryset().select_related(
                'type_airplane',
                'arrival_city',
                'dispatch_city',
                'status',
            )

    def get_context_data(self, **kwargs):
        context = super(FlightListView, self).get_context_data(**kwargs)
        form = self.form_class()
        context['form'] = form
        context['q'] = self.request.GET.get('q')
        return context


class Search(FlightListView):
    paginate_by = 5

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            logger.debug('запрос страницы {1} на получение рейсов с параметрами: {0}'
                         .format(form.cleaned_data['q'].encode('utf-8'),
                                 self.request.GET.get(self.page_kwarg, 1)))
            return super(FlightListView, self).get_queryset().select_related(
                'type_airplane',
                'arrival_city',
                'dispatch_city',
                'status',
            ).filter(
                Q(arrival_city__name__icontains=form.cleaned_data['q']) |
                Q(dispatch_city__name__icontains=form.cleaned_data['q']) |
                Q(status__title__icontains=form.cleaned_data['q'])
            )
        return super(FlightListView, self).get_queryset().select_related(
            'type_airplane',
            'arrival_city',
            'dispatch_city',
            'status',
        )


class CreateFlightView(LoginRequiredMixin, CreateView):
    model = Flight
    template_name = 'flight_scoreboard/create_flight.html'
    form_class = CreateFlightForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            flight = form.save()
            instance = Flight.objects.only('id').get(pk=flight.id)
            logger.debug('создание нового объекта flight c id: {}'.format(instance.id))
            return redirect(reverse('flight_scoreboard:flight_list'))
        else:
            logger.debug('не удачная попытка создания нового объекта flight')
            return super(CreateFlightView, self).get(request)


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

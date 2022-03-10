#-*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import re

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import CASCADE, PROTECT


def is_correct_number(number):
    if not re.match(r'\w\w\d{4}$', number):
        raise ValidationError('не правильный номер')


class Flight(models.Model):
    number = models.CharField(
        unique=True,
        max_length=10,
        verbose_name='номер самолета',
        validators=[is_correct_number, ]
    )
    type_airplane = models.ForeignKey('TypeAirplane', on_delete=CASCADE, verbose_name='тип самолета')
    arrival_city = models.ForeignKey(
        'City',
        on_delete=CASCADE,
        verbose_name='город прибытия'
    )
    dispatch_city = models.ForeignKey(
        'City',
        on_delete=CASCADE,
        related_name='dispatch',
        verbose_name='город отправки'
    )
    status = models.ForeignKey('Status', on_delete=PROTECT, null=True, verbose_name='статус')
    departure_time = models.DateTimeField(verbose_name='время отправления')
    arrival_time = models.DateTimeField(verbose_name='время прибытия')
    actual_time = models.DateTimeField(verbose_name='фактическое время', blank=True, null=True)

    class Meta:
        verbose_name = 'рейс'
        verbose_name_plural = 'рейсы'
        ordering = ['-departure_time', '-arrival_time', ]

    def __str__(self):
        return 'Рейс №{}'.format(self.number).encode('utf-8')

    def get_absolute_url(self):
        return reverse('flight_scoreboard:current_flight', kwargs={'pk': self.pk})

    def clean(self):
        if self.departure_time > self.arrival_time:
            raise ValidationError('Дата отправления не может быть позже даты прибытия')
        if self.arrival_city == self.dispatch_city:
            raise ValidationError('города отправления/прибытия должны быть разными')


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='город')

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'

    def __str__(self):
        return self.name.encode('utf-8')


class Status(models.Model):
    title = models.CharField(max_length=50, verbose_name='название')

    class Meta:
        verbose_name = 'статус'
        verbose_name_plural = 'статусы'

    def __str__(self):
        return self.title.encode('utf-8')


class TypeAirPlane(models.Model):
    title = models.CharField(max_length=50, verbose_name='тип самолета')

    class Meta:
        verbose_name = 'тип самолета'
        verbose_name_plural = 'типы самолетов'

    def __str__(self):
        return self.title.encode('utf-8')
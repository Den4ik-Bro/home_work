# coding=utf-8
from __future__ import unicode_literals

import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CASCADE, PROTECT


class Flight(models.Model):
    number = models.CharField(max_length=10, verbose_name='номер самолета')
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
    departure_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='время отправления')
    arrival_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='время прибытия')
    actual_time = models.DateTimeField(verbose_name='фактическое время', blank=True, null=True)

    class Meta:
        verbose_name = 'рейс'
        verbose_name_plural = 'рейсы'

    def __str__(self):
        return 'Рейс №{}'.format(self.number).encode('utf-8')

    def clean(self):
        if self.departure_time > self.arrival_time:
            raise ValidationError('Дата отправления не может быть позже даты прибытия')


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
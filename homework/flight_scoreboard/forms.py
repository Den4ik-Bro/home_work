#-*- coding: utf-8 -*-
from django.contrib.admin.widgets import AdminSplitDateTime
from django.core.exceptions import ValidationError
from django.forms import fields

from . import models
from django import forms


class CreateFlightForm(forms.ModelForm):
    arrival_time = fields.DateTimeField(
        widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        label='Время прибытия'
    )
    departure_time = fields.DateTimeField(
        widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        label='Время отправления'
    )

    class Meta:
        model = models.Flight
        fields = '__all__'


def validate_search_query(value):
    if len(value) == 0:
        raise ValidationError('поле не может быть пустым')


class SearchForm(forms.Form):
    q = forms.CharField(
        max_length=20,
        min_length=1,
        label='поиск',
        required=True,
        validators=[validate_search_query, ]
    )

    # def clean_q(self):
    #     data = self.cleaned_data['q']
    #     if len(data) == 0:
    #         raise ValidationError('Поле не может быть пустым')
    #     return data


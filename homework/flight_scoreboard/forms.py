#-*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from . import models
from django import forms
from .models import Flight


class CreateFlightForm(forms.ModelForm):

    class Meta:
        model = models.Flight
        fields = '__all__'


def validate_search_query(value):
    print value
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




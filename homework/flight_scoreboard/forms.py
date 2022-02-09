# coding=utf-8
from django.core.exceptions import ValidationError

from . import models
from django import forms


class CreateFlightForm(forms.ModelForm):

    class Meta:
        model = models.Flight
        fields = '__all__'


class SearchForm(forms.Form):
    q = forms.CharField(max_length=20, validators=[], label='поиск')





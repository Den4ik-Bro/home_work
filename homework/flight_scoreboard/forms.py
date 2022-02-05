from . import models
from django import forms


class CreateFlightForm(forms.ModelForm):

    class Meta:
        model = models.Flight
        fields = '__all__'



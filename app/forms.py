from django.forms import ModelForm
from .models import Sale, FuelLitre

class SaleForm(ModelForm):

    class Meta:
        model = Sale
        fields = ['total_sold_litres']


class FuelLitreForm(ModelForm):

    class Meta:
        model = FuelLitre
        fields = ['fuel_litres']




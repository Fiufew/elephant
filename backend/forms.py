from django import forms
from .models import Car, Bid


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ('slug',)


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = '__all__'

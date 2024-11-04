from django import forms

from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from .models import Car, Bid


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ('slug',)


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = '__all__'
        widgets = {
            'pickup_time': DateTimePickerInput(
                options={
                    'format': 'YYYY-MM-DD HH:mm:ss',
                    'locale': 'ru',
                }
            ),
            'dropoff_time': DateTimePickerInput(
                options={
                    'format': 'YYYY-MM-DD HH:mm:ss',
                    'locale': 'ru',
                }
            ),
        }

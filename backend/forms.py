from django import forms

from .models import Car, Price


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'category', 'color', 'brand',
            'model', 'investor',
            ]
        labels = {
            'category': 'Категория',
            'color': 'Цвет',
            'brand': 'Бренд',
            'model': 'Модель',
            'investor': 'Инвестор',
        }


class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = ['winter_price', 'spring_price', 'summer_price',
                  'autumn_price', 'currency']

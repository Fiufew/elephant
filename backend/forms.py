from django import forms
from bootstrap_datepicker_plus.widgets import (
    DateTimePickerInput, DatePickerInput)

from .models import Car, Price, Insurance, Application


class CarForm(forms.ModelForm):
    insurance_symbol = forms.CharField(
        max_length=128,
        required=False,
        label='Номер страховки'
    )
    insurance_start_date = forms.DateTimeField(
        required=False,
        label='Начало страховки',
        widget=DateTimePickerInput(
            options={
                'format': 'DD.MM.YYYY HH:mm',
                'locale': 'ru',
            }
        )
    )
    insurance_expired_date = forms.DateTimeField(
        required=False,
        label='Окончание страховки',
        widget=DateTimePickerInput(
            options={
                'format': 'DD.MM.YYYY HH:mm',
                'locale': 'ru',
            }
        )
    )

    def save(self, commit=True):
        car = super().save(commit=False)
        insurance_symbol = self.cleaned_data.get('insurance_symbol')
        insurance_start_date = self.cleaned_data.get('insurance_start_date')
        insurance_expired_date = self.cleaned_data.get(
            'insurance_expired_date')

        if insurance_symbol and (
            insurance_start_date and
                insurance_expired_date):
            insurance, created = Insurance.objects.get_or_create(
                symbol=insurance_symbol,
                start_date=insurance_start_date,
                expired_date=insurance_expired_date
            )
            car.insurance = insurance
        else:
            insurance = Insurance.objects.create(
                symbol='',
                start_date=None,
                expired_date=None
            )
            car.insurance = insurance

        if commit:
            car.save()
        return car

    class Meta:
        model = Car
        fields = [
            'category', 'color', 'brand',
            'model', 'license_plate', 'investor',
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
        fields = [
            'winter_price', 'spring_price', 'summer_price',
            'autumn_price', 'currency']


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'car', 'pickup_location', 'dropoff_location',
            'pickup_time', 'dropoff_time', 'renter_name',
            'renter_phone', 'renter_email', 'comment',
            'aggregator_id', 'aggregator'
            ]
        labels = {
            'car': 'Автомобиль',
            'pickup_location': 'Место получения',
            'dropoff_location': 'Место возврата',
            'pickup_time': 'Время получения',
            'dropoff_time': 'Время возврата',
            'renter_name': 'Имя арендатора',
            'renter_phone': 'Телефон арендатора',
            'renter_email': 'Email арендатора',
            'aggregator_id': 'Номер заявки аггрегатора',
            'aggregator': 'Аггрегатор',
            'comment': 'Комментарий',
            'application_preparer': 'Подготовитель заявки',
            'contract': 'Договор',
            'vaucher': 'Ваучер'
        }
        widgets = {
            'pickup_time': DateTimePickerInput(
                options={
                    'format': 'DD.MM.YYYY HH:mm',
                    'locale': 'ru',
                }
            ),
            'dropoff_time': DateTimePickerInput(
                options={
                    'format': 'DD.MM.YYYY HH:mm',
                    'locale': 'ru',
                }
            ),
            'renter_birthdate': DatePickerInput(
                options={
                    'format': 'YYYY.MM.DD',
                    'locale': 'ru',
                }
            ),
            'aggregator': forms.Select(choices=Application.AGGREGATOR_CHOICES),
        }
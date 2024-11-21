from django import forms
from django.core.exceptions import ValidationError

from bootstrap_datepicker_plus.widgets import (
    DateTimePickerInput,
    DatePickerInput
    )
from .models import Car, Bid, Files, Price
from .validators import contains_digits


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'category', 'color', 'brand',
            'model', 'investor', 'is_booked',
            'insurance', 'description',
            'state_number', 'photo'
            ]
        labels = {
            'category': 'Категория',
            'color': 'Цвет',
            'brand': 'Бренд',
            'model': 'Модель',
            'investor': 'Инвестор',
            'is_booked': 'Забронирован',
            'insurance': 'Страховка',
            'description': 'Описание',
            'state_number': 'Гос. номер',
            'photo': 'Фото',
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = [
            'car', 'pickup_location', 'dropoff_location',
            'pickup_time', 'dropoff_time', 'renter_name', 'renter_birthdate',
            'renter_phone', 'renter_email', 'contact_method',
            'comment'
            ]
        labels = {
            'car': 'Автомобиль',
            'pickup_location': 'Место получения',
            'dropoff_location': 'Место возврата',
            'pickup_time': 'Время получения',
            'dropoff_time': 'Время возврата',
            'renter_name': 'Имя арендатора',
            'renter_birthdate': 'Дата рождения арендатора',
            'renter_phone': 'Телефон арендатора',
            'renter_email': 'Email арендатора',
            'contact_method': 'Метод контакта',
            'comment': 'Комментарий',
            'bid_preparer': 'Подготовитель заявки',
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
        }

    def clean(self):
        cleaned_data = super().clean()
        car = cleaned_data.get('car')
        pickup_location = cleaned_data.get('pickup_location')
        dropoff_location = cleaned_data.get('dropoff_location')
        renter_name = cleaned_data.get('renter_name')
        pickup_time = cleaned_data.get('pickup_time')
        dropoff_time = cleaned_data.get('dropoff_time')
        if pickup_time and dropoff_time:
            if dropoff_time <= pickup_time:
                raise ValidationError(
                    'Дата возврата должна быть позже даты получения.')
            existing_bids = Bid.objects.filter(
                car=car,
                pickup_time__lte=dropoff_time,
                dropoff_time__gte=pickup_time
            )
        if existing_bids.exists():
            raise ValidationError(
                'Выбранные даты пересекаются с '
                'уже существующими бронированиями.')
        if pickup_location and contains_digits(pickup_location):
            raise ValidationError(
                'Место получения не может содержать цифры.')
        if dropoff_location and contains_digits(dropoff_location):
            raise ValidationError(
                'Место возврата не может содержать цифры.')
        if renter_name and contains_digits(renter_name):
            raise ValidationError(
                'Имя не может содержать цифры. '
                'Только если ты не сын Илона Маска')
        return cleaned_data


class BidFormAddFiles(forms.ModelForm):
    class Meta:
        model = Files
        fields = ['files']


class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        exclude = ('car_price',)

from django import forms
from django.core.exceptions import ValidationError

from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from .models import Car, Bid


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['category', 'color', 'brand',
                  'model', 'investor', 'is_booked',
                  'insurance', 'description',
                  'state_number', 'photo']
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
        fields = ['car', 'pickup_location', 'dropoff_location', 'pickup_time',
                  'dropoff_time', 'renter_name', 'renter_birthdate',
                  'renter_phone', 'renter_email', 'contact_method',
                  'comment', 'bid_preparer', 'contract', 'vaucher']
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
            'doc': 'Договор'
        }
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

    def clean(self):
        cleaned_data = super().clean()
        car = cleaned_data.get('car')
        pickup_time = cleaned_data.get('pickup_time')
        dropoff_time = cleaned_data.get('dropoff_time')
        if pickup_time and dropoff_time:
            if dropoff_time <= pickup_time:
                raise ValidationError('Дата возврата должна быть позже даты получения.')
            existing_bids = Bid.objects.filter(
                car=car,
                pickup_time__lte=dropoff_time,
                dropoff_time__gte=pickup_time
            )
            if existing_bids.exists():
                raise ValidationError('Выбранные даты пересекаются с уже существующими бронированиями.')
        return cleaned_data


class BidFormAddFiles(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['files']

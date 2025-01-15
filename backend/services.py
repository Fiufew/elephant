from django.shortcuts import redirect
from .models import Application, Price


class ApplicationService:

    @staticmethod
    def take_in_work(pk, username):
        try:
            application = Application.objects.get(id=pk)
            application.bid_preparer = username  # подготовитель заявки == пользователь от имени которого получен запрос
            application.save()
        except Application.DoesNotExist:
            pass
        return redirect('backend:bid_list')


class PriceService:

    @staticmethod
    def create_price(car, price_data):
        price = Price(car_price=car, **price_data)
        price.save()
        return price

    @staticmethod
    def update_price(price, price_data):
        for key, value in price_data.items():
            setattr(price, key, value)
        price.save()
        return price

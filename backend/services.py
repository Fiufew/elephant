from django.shortcuts import redirect
from django.db.models import Q
from .models import Application, Price, Car


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


class CarService:

    @staticmethod
    def get_filtered_cars(search_query, booked_only):
        cars = Car.objects.select_related('brand', 'model', 'color').all()
        if search_query:
            cars = cars.filter(
                Q(brand__name__icontains=search_query) |
                Q(model__name__icontains=search_query) |
                Q(category__name__icontains=search_query) |
                Q(year_manufactored__icontains=search_query) |
                Q(license_plate__icontains=search_query)
            )
        if booked_only:
            cars = Car.objects.available_cars()
        return cars


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

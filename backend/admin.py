from django.contrib import admin
from .models import (Category, Color, Brand, Model, Car,
                     Price, Application, Investor, Insurance)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ('symbol',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'is_availaible',
                    'created_at', 'updated_at')
    list_filter = ('brand', 'model', 'is_availaible')
    exclude = ('car_name',)
    search_fields = ('brand__name', 'model__name', 'license_plate')


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('winter_price', 'spring_price',
                    'summer_price', 'autumn_price',
                    'currency', 'car_price')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('car', 'price', 'pickup_location',
                    'dropoff_location', 'pickup_time', 'dropoff_time',
                    'renter_name', 'renter_phone',
                    'renter_email',
                    'comment', 'is_expired')
    list_filter = ('car', 'price')

from django.contrib import admin

from .models import (
    Application, Brand,
    Car, Category, Color,
    Insurance, Investor,
    Model, Problem)


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
    list_display = (
        'brand', 'model', 'is_availaible',
        'created_at', 'updated_at')
    list_filter = ('brand', 'model', 'is_availaible')
    exclude = ('car_name',)
    search_fields = ('brand__name', 'model__name', 'license_plate')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'car', 'price', 'pickup_location',
        'dropoff_location', 'pickup_time', 'dropoff_time',
        'renter_name', 'renter_phone',
        'renter_email',
        'comment', 'status')
    list_filter = ('car', 'price')


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('issue', 'is_solved')

from django.contrib import admin
from .models import (
    Brand, CarModel, Problem, Engine, ACT,
    Photo, Car, Price, Application, Date, Misc,
    Chassis, Music, Other, FirstClass, SecondClass,
    Tax
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_solved', 'created_at', 'solved_at')
    list_filter = ('is_solved',)
    search_fields = ('name',)


@admin.register(Engine)
class EngineAdmin(admin.ModelAdmin):
    list_display = ('engine_type', 'capacity', 'fuel', 'tank', 'fuel_consumption')
    list_filter = ('fuel',)


@admin.register(Chassis)
class ChassisAdmin(admin.ModelAdmin):
    list_display = ('transmission', 'drive', 'chassis_abs', 'chassis_ebd', 'chassis_esp')
    list_filter = ('transmission', 'drive')


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ('radio', 'audio_cd', 'audio_mp3', 'audio_usb', 'audio_aux', 'audio_bluetooth')


@admin.register(Other)
class OtherAdmin(admin.ModelAdmin):
    list_display = ('category_drivers_license', 'seats', 'doors', 'air_conditioner', 'cruise_control')


@admin.register(ACT)
class ACTAdmin(admin.ModelAdmin):
    list_display = ('number', 'is_expired', 'expired_at')
    list_filter = ('is_expired',)


@admin.register(FirstClass)
class FirstClassAdmin(admin.ModelAdmin):
    list_display = ('number', 'is_expired', 'expired_at')
    list_filter = ('is_expired',)


@admin.register(SecondClass)
class SecondClassAdmin(admin.ModelAdmin):
    list_display = ('number', 'is_expired', 'expired_at')
    list_filter = ('is_expired',)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('number', 'is_expired', 'expired_at')
    list_filter = ('is_expired',)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('car_image',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'number', 'year_manufactured', 'body_type', 'color', 'created_at')
    list_filter = ('brand', 'model', 'body_type', 'color', 'year_manufactured')
    search_fields = ('brand__name', 'model__name', 'number')


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('pick_season', 'high_season', 'low_season', 'currency')
    list_filter = ('currency',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('num', 'auto', 'aggregator', 'date', 'location_delivery', 'location_return', 'price', 'currency')
    list_filter = ('aggregator', 'currency', 'date')
    search_fields = ('num', 'auto__brand__name', 'auto__model__name')


@admin.register(Date)
class DateAdmin(admin.ModelAdmin):
    list_display = ('application', 'date_delivery', 'date_return')
    list_filter = ('date_delivery', 'date_return')


@admin.register(Misc)
class MiscAdmin(admin.ModelAdmin):
    list_display = ('application', 'contract', 'vaucher', 'video')

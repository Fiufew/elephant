from django.contrib import admin
from .models import (
    CarBrand, CarModel, Problem,
    Engine, Act, Photo,
    Car, Application,
    Date, Misc, Chassis,
    Music, Other, FirstClass,
    SecondClass, Tax
)


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    search_fields = (
        'name',
    )


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    search_fields = (
        'name',
    )


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'is_solved', 'created_at',
        'solved_at',
    )
    list_filter = (
        'is_solved',
    )
    search_fields = (
        'name',
    )


@admin.register(Engine)
class EngineAdmin(admin.ModelAdmin):
    list_display = (
        'capacity', 'fuel', 'tank',
        'fuel_consumption', 'power',
    )
    list_filter = (
        'fuel',
    )


@admin.register(Chassis)
class ChassisAdmin(admin.ModelAdmin):
    list_display = (
        'transmission', 'drive', 'chassis_abs',
        'chassis_ebd', 'chassis_esp',
    )
    list_filter = (
        'transmission', 'drive',
    )


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = (
        'radio', 'audio_cd', 'audio_mp3',
        'audio_usb', 'audio_aux', 'audio_bluetooth',
    )


@admin.register(Other)
class OtherAdmin(admin.ModelAdmin):
    list_display = (
        'category_drivers_license', 'seats', 'doors',
        'air_conditioner', 'cruise_control',
    )


@admin.register(Act)
class ActAdmin(admin.ModelAdmin):
    list_display = (
        'is_expired', 'expired_at',
    )
    list_filter = (
        'is_expired',
    )


@admin.register(FirstClass)
class FirstClassAdmin(admin.ModelAdmin):
    list_display = (
        'is_expired', 'expired_at',
    )
    list_filter = (
        'is_expired',
    )


@admin.register(SecondClass)
class SecondClassAdmin(admin.ModelAdmin):
    list_display = (
        'is_expired', 'expired_at',
    )
    list_filter = ('is_expired',)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = (
        'is_expired', 'expired_at',
    )
    list_filter = (
        'is_expired',
    )


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        'car_image',
    )


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'brand', 'model', 'number',
        'year_manufactured', 'body_type', 'color',
        'created_at',
    )
    list_filter = (
        'brand', 'model', 'body_type',
        'color', 'year_manufactured',
    )
    search_fields = (
        'brand__name', 'model__name', 'number',
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'num', 'agregator', 'auto',
        'status', 'location_delivery', 'url_delivery',
        'location_return', 'url_return', 'client_name',
        'birthdate', 'contacts', 'contact_type',
        'client_email', 'deposit_in_hand', 'currency',
        'price', 'baby_seat', 'another_regions',
        'complex_insurance',
    )
    list_filter = (
        'agregator', 'currency',
    )
    search_fields = (
        'num', 'auto__brand__name', 'auto__model__name',
    )


@admin.register(Date)
class DateAdmin(admin.ModelAdmin):
    list_display = (
        'application', 'date_delivery', 'date_return',
    )
    list_filter = (
        'date_delivery', 'date_return',
    )


@admin.register(Misc)
class MiscAdmin(admin.ModelAdmin):
    list_display = (
        'application', 'contract', 'vaucher',
        'other_files',
    )

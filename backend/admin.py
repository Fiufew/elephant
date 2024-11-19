from django.contrib import admin

from .models import Category, Color, Brand, Model, Car, Price, Bid, Investor


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
    list_display = ('brand', 'model', 'is_booked', 'created_at', 'updated_at')
    list_filter = ('brand', 'model', 'is_booked')
    exclude = ('slug',)
    search_fields = ('brand__name', 'model__name', 'state_number')


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('car_price', 'season_one',
                    'season_two', 'season_three',
                    'season_four')


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('car', 'pickup_location',
                    'dropoff_location', 'pickup_time', 'dropoff_time',
                    'renter_name',
                    'renter_birthdate', 'renter_phone', 'renter_email',
                    'contact_method', 'comment', 'bid_preparer', 'is_expired')
    list_filter = ('car', 'contact_method')
    search_fields = ('renter_name', 'renter_email', 'bid_preparer')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "price":
            kwargs["queryset"] = Price.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

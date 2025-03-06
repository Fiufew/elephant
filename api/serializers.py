from rest_framework import serializers
from rest_framework.serializers import (
    PrimaryKeyRelatedField,
    StringRelatedField,
    SerializerMethodField
    )

from backend.models import (
    Brand, CarModel, Problem,
    Engine, Music, Other,
    Insurance, Photo, Chassis,
    Car, Price
    )


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['name']


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = [
            'name', 'is_solved',
            'created_at', 'solved_at'
        ]


class EngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engine
        fields = [
            'engine_type', 'capacity',
            'fuel', 'tank',
            'fuel_consumption'
        ]


class ChassisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chassis
        fields = [
            'transmission', 'drive',
            'chassis_abs', 'chassis_ebd',
            'chassis_esp'
        ]


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = [
            'radio', 'audio_cd',
            'audio_mp3', 'audio_usb',
            'audio_aux', 'audio_bluetooth'
        ]


class OtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Other
        fields = [
            'category_drivers_license', 'seats',
            'doors', 'air_conditioner',
            'interior', 'roof',
            'powered_window', 'airbags',
            'side_wheel', 'cruise_control',
            'rear_view_camera', 'parking_assist'
        ]


class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = [
            'number', 'is_expired',
            'expired_at'
        ]


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = [
            'car_image'
        ]


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = [
            'car_price', 'winter_price',
            'spring_price', 'summer_price',
            'autumn_price', 'currency'
        ]


class CarSerializer(serializers.ModelSerializer):
    brand = StringRelatedField()
    model = StringRelatedField()
    price = SerializerMethodField()
    insurance = InsuranceSerializer(read_only=True)
    engine = EngineSerializer(read_only=True)
    chassis = ChassisSerializer(read_only=True)
    music = MusicSerializer(read_only=True)
    other = OtherSerializer(read_only=True)
    photos = SerializerMethodField()
    problems = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Car
        fields = [
            'brand', 'model',
            'insurance', 'engine',
            'chassis', 'music',
            'other', 'photos',
            'problems', 'number',
            'year_manufactured', 'body_type',
            'deposit', 'color',
            'created_at', 'updated_at'
        ]

    def get_price(self, obj):
        price = obj.price
        return PriceSerializer(price).data if price else None

    def get_photos(self, obj):
        photos = obj.photos.all()
        return [photo.car_image.url for photo in photos] if photos else []

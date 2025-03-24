from rest_framework import serializers

from users.models import CustomElephantUser
from items.models import (
    Brand, CarModel, Problem,
    Engine, Chassis,
    Insurance, Photo,
    Car, Price, Date,
    Music, Other, Application,
    Misc
    )


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['name']


class CarRentalDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = ["date_delivery", "date_return"]


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
            'winter_price',
            'spring_price', 'summer_price',
            'autumn_price', 'currency'
        ]


class MiscSerializer(serializers.ModelSerializer):
    class Meta:
        model = Misc
        fields = ['contract', 'vaucher', 'video']
        extra_kwargs = {
            'contract': {'required': False, 'allow_null': True},
            'vaucher': {'required': False, 'allow_null': True},
            'video': {'required': False, 'allow_null': True},
        }


class CarSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    model = CarModelSerializer()
    price = PriceSerializer()
    insurance = InsuranceSerializer()
    engine = EngineSerializer()
    chassis = ChassisSerializer()
    music = MusicSerializer()
    other = OtherSerializer()
    photos = PhotoSerializer(many=True)
    problems = ProblemSerializer(many=True)

    class Meta:
        model = Car
        fields = [
            'id',
            'brand', 'model',
            'insurance', 'engine',
            'photos', 'price',
            'chassis', 'music',
            'other',
            'problems', 'number',
            'year_manufactured', 'body_type',
            'deposit', 'color',
            'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        brand_data = validated_data.pop('brand')
        model_data = validated_data.pop('model')
        price_data = validated_data.pop('price')
        insurance_data = validated_data.pop('insurance')
        engine_data = validated_data.pop('engine')
        chassis_data = validated_data.pop('chassis')
        photos_data = validated_data.pop('photos')
        problems_data = validated_data.pop('problems')
        music_data = validated_data.pop('music')
        other_data = validated_data.pop('other')

        brand = Brand.objects.create(**brand_data)
        model = CarModel.objects.create(**model_data)
        price = Price.objects.create(**price_data)
        insurance = Insurance.objects.create(**insurance_data)
        engine = Engine.objects.create(**engine_data)
        chassis = Chassis.objects.create(**chassis_data)
        music = Music.objects.create(**music_data)
        other = Other.objects.create(**other_data)

        car = Car.objects.create(
            brand=brand,
            model=model,
            price=price,
            insurance=insurance,
            engine=engine,
            chassis=chassis,
            music=music,
            other=other,
            **validated_data
        )
        if price_data:
            Price.objects.create(car_price=car, **price_data)

        for photo_data in photos_data:
            Photo.objects.create(car=car, **photo_data)

        for problem_data in problems_data:
            Problem.objects.create(car=car, **problem_data)

        return car


class ApplicationSerializer(serializers.ModelSerializer):
    rental_dates = CarRentalDatesSerializer(required=False)
    misc_files = MiscSerializer()

    def create(self, validated_data):
        rental_dates_data = validated_data.pop('rental_dates')
        misc_data = validated_data.pop('misc_files', None)
        application = Application.objects.create(
            **validated_data
        )
        if rental_dates_data:
            Date.objects.create(application=application, **rental_dates_data)
        if misc_data:
            Misc.objects.create(application=application, **misc_data)

        return application

    class Meta:
        model = Application
        fields = [
            'num', 'aggregator', 'date', 'auto', 'location_delivery',
            'location_return', 'name', 'contacts', 'deposit_in_hand',
            'currency', 'price', 'rental_dates', 'birthdate',
            'contact_type', 'client_email', 'status', 'misc_files'
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomElephantUser
        fields = ['username', 'password']

    def create(self, validated_data):
        user = CustomElephantUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

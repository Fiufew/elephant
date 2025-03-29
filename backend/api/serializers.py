from rest_framework import serializers

from users.models import CustomElephantUser
from items.models import (
    CarBrand, CarModel, Problem,
    Engine, Chassis, FirstClass,
    ACT, Photo, SecondClass,
    Car, Price, Date,
    Music, Other, Application,
    Misc, Tax
    )


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
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
            'power', 'capacity',
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


class ACTSerializer(serializers.ModelSerializer):
    class Meta:
        model = ACT
        fields = [
            'name', 'is_expired',
            'expired_at'
        ]


class FirstClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirstClass
        fields = [
            'name', 'is_expired',
            'expired_at'
        ]


class SecondClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondClass
        fields = [
            'name', 'is_expired',
            'expired_at'
        ]


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = [
            'name', 'is_expired',
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
            'pick_season',
            'high_season', 'low_season',
            'currency'
        ]


class MiscSerializer(serializers.ModelSerializer):
    class Meta:
        model = Misc
        fields = ['contract', 'vaucher', 'other_files']
        extra_kwargs = {
            'contract': {'required': False, 'allow_null': True},
            'vaucher': {'required': False, 'allow_null': True},
            'other_files': {'required': False, 'allow_null': True},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['contract'] = request.FILES.get('contract')
        validated_data['vaucher'] = request.FILES.get('vaucher')
        validated_data['other_files'] = request.FILES.get('other_files')
        return super().create(validated_data)


class CarSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    model = CarModelSerializer()
    price = PriceSerializer()
    act = ACTSerializer()
    first_class = FirstClassSerializer()
    second_class = SecondClassSerializer()
    tax = TaxSerializer()
    engine = EngineSerializer()
    chassis = ChassisSerializer()
    music = MusicSerializer()
    other = OtherSerializer()
    photos = PhotoSerializer()
    problems = ProblemSerializer()

    class Meta:
        model = Car
        fields = [
            'id',
            'brand', 'model',
            'engine',
            'photos', 'price',
            'chassis', 'music',
            'other', 'act', 'first_class',
            'second_class', 'tax',
            'problems', 'number',
            'year_manufactured', 'body_type',
            'deposit', 'color',
            'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        print("Validated Data:", validated_data)
        brand_data = validated_data.pop('brand')
        model_data = validated_data.pop('model')
        price_data = validated_data.pop('price')
        act_data = validated_data.pop('act')
        first_class_data = validated_data.pop('first_class')
        second_class_data = validated_data.pop('second_class')
        tax_data = validated_data.pop('tax')
        engine_data = validated_data.pop('engine')
        chassis_data = validated_data.pop('chassis')
        music_data = validated_data.pop('music')
        other_data = validated_data.pop('other')
        photos_data = validated_data.pop('photos', [])
        problems_data = validated_data.pop('problems', [])
        brand = CarBrand.objects.create(**brand_data)
        model = CarModel.objects.create(**model_data)
        price = Price.objects.create(**price_data)
        act = ACT.objects.create(**act_data)
        first_class = FirstClass.objects.create(**first_class_data)
        second_class = SecondClass.objects.create(**second_class_data)
        tax = Tax.objects.create(**tax_data)
        engine = Engine.objects.create(**engine_data)
        chassis = Chassis.objects.create(**chassis_data)
        music = Music.objects.create(**music_data)
        other = Other.objects.create(**other_data)

        car = Car.objects.create(
            brand=brand,
            model=model,
            price=price,
            act=act,
            first_class=first_class,
            second_class=second_class,
            tax=tax,
            engine=engine,
            chassis=chassis,
            music=music,
            other=other,
            **validated_data
        )
        if isinstance(photos_data, list):
            for photo_data in photos_data:
                if isinstance(photo_data, dict) and photo_data.get("car_image"):
                    Photo.objects.create(car=car, **photo_data)
        if isinstance(problems_data, list):
            for problem_data in problems_data:
                if isinstance(problem_data, dict):
                    Problem.objects.create(car=car, **problem_data)
        return car


class ApplicationSerializer(serializers.ModelSerializer):
    contract = serializers.FileField(required=False, allow_null=True)
    vaucher = serializers.FileField(required=False, allow_null=True)
    other_files = serializers.FileField(required=False, allow_null=True)
    bluebook = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Application
        fields = [
            'num', 'aggregator', 'auto', 'location_delivery',
            'location_return', 'contacts', 'deposit_in_hand',
            'currency', 'price', 'birthdate',
            'contact_type', 'client_email', 'status',
            'contract', 'vaucher', 'other_files'
        ]

    def create(self, validated_data):
        contract = validated_data.pop('contract', None)
        vaucher = validated_data.pop('vaucher', None)
        other_files = validated_data.pop('other_files', None)
        bluebook = validated_data.pop('bluebook', None)
        application = Application.objects.create(**validated_data)
        if contract:
            application.contract = contract
        if vaucher:
            application.vaucher = vaucher
        if other_files:
            application.other_files = other_files
        if bluebook:
            application.bluebook = bluebook
        application.save()
        return application


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

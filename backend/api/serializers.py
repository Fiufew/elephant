from rest_framework import serializers

from users.models import CustomElephantUser
from items.models import (
    CarBrand, CarModel, Problem,
    Engine, Chassis, FirstClass,
    Act, Photo, SecondClass,
    Car, Price, Date,
    Music, Other, Application,
    Misc, Tax, Bluebook
    )


class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = [
            'name',
        ]


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = [
            'name',
        ]


class CarRentalDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = [
            'date_delivery', 'date_return',
        ]


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = [
            'name', 'is_solved', 'created_at',
            'solved_at',
        ]


class EngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engine
        fields = [
            'power', 'capacity', 'fuel',
            'tank', 'fuel_consumption',
        ]


class ChassisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chassis
        fields = [
            'transmission', 'drive', 'chassis_abs',
            'chassis_ebd', 'chassis_esp',
        ]


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = [
            'radio', 'audio_cd', 'audio_mp3',
            'audio_usb', 'audio_aux', 'audio_bluetooth',
        ]


class OtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Other
        fields = [
            'category_drivers_license', 'seats', 'doors',
            'air_conditioner', 'interior', 'roof',
            'powered_window', 'airbags', 'side_wheel',
            'cruise_control', 'rear_view_camera', 'parking_assist',
        ]


class ActSerializer(serializers.ModelSerializer):
    class Meta:
        model = Act
        fields = [
            'is_expired', 'expired_at',
        ]


class FirstClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirstClass
        fields = [
            'is_expired', 'expired_at',
        ]


class SecondClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondClass
        fields = [
            'is_expired', 'expired_at',
        ]


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = [
            'is_expired', 'expired_at',
        ]


class BluebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bluebook
        fields = [
            'is_expired', 'expired_at', 'bluebook_image',
        ]


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = [
            'id', 'car_image',
        ]
        extra_kwargs = {
            'car_image': {'required': False, 'allow_null': True}
        }


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = [
            'pick_season', 'high_season', 'low_season',
        ]


class MiscSerializer(serializers.ModelSerializer):
    class Meta:
        model = Misc
        fields = [
            'contract', 'vaucher', 'other_files',
        ]
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
    brand = CarBrandSerializer()
    model = CarModelSerializer()
    price = PriceSerializer()
    engine = EngineSerializer()
    chassis = ChassisSerializer()
    music = MusicSerializer()
    other = OtherSerializer()
    photos = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )
    bluebook = serializers.FileField(required=False, write_only=True)
    act_data = ActSerializer(required=False, write_only=True)
    first_class_data = FirstClassSerializer(required=False, write_only=True)
    second_class_data = SecondClassSerializer(required=False, write_only=True)
    tax_data = TaxSerializer(required=False, write_only=True)

    class Meta:
        model = Car
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        brand_data = validated_data.pop('brand')
        model_data = validated_data.pop('model')
        price_data = validated_data.pop('price')
        engine_data = validated_data.pop('engine')
        chassis_data = validated_data.pop('chassis')
        music_data = validated_data.pop('music')
        other_data = validated_data.pop('other')
        act_data = validated_data.pop('act_data', None)
        first_class_data = validated_data.pop('first_class_data', None)
        second_class_data = validated_data.pop('second_class_data', None)
        tax_data = validated_data.pop('tax_data', None)
        photos = validated_data.pop('photos', [])
        bluebook_file = validated_data.pop('bluebook', None)

        brand = CarBrand.objects.create(**brand_data)
        model = CarModel.objects.create(**model_data)
        price = Price.objects.create(**price_data)
        engine = Engine.objects.create(**engine_data)
        chassis = Chassis.objects.create(**chassis_data)
        music = Music.objects.create(**music_data)
        other = Other.objects.create(**other_data)

        car = Car.objects.create(
            brand=brand,
            model=model,
            price=price,
            engine=engine,
            chassis=chassis,
            music=music,
            other=other,
            **validated_data
        )

        if act_data:
            Act.objects.create(car=car, **act_data)
        if first_class_data:
            FirstClass.objects.create(car=car, **first_class_data)
        if second_class_data:
            SecondClass.objects.create(car=car, **second_class_data)
        if tax_data:
            Tax.objects.create(car=car, **tax_data)
        if bluebook_file:
            Bluebook.objects.create(car=car, bluebook_image=bluebook_file)
        for photo in photos:
            Photo.objects.create(car=car, car_image=photo)
        return car


class ApplicationSerializer(serializers.ModelSerializer):
    contract = serializers.FileField(required=False, allow_null=True, write_only=True)
    vaucher = serializers.FileField(required=False, allow_null=True, write_only=True)
    other_files = serializers.FileField(required=False, allow_null=True, write_only=True)

    class Meta:
        model = Application
        fields = [
            'num', 'agregator', 'auto',
            'status', 'location_delivery', 'url_delivery',
            'location_return', 'url_return', 'client_name',
            'birthdate', 'contacts', 'contact_type',
            'client_email', 'deposit_in_hand', 'currency',
            'price', 'baby_seat', 'another_regions',
            'complex_insurance', 'contract', 'vaucher',
            'other_files',
        ]

    def create(self, validated_data):
        contract = validated_data.pop('contract', None)
        vaucher = validated_data.pop('vaucher', None)
        other_files = validated_data.pop('other_files', None)

        application = Application.objects.create(**validated_data)
        Misc.objects.create(
            application=application,
            contract=contract,
            vaucher=vaucher,
            other_files=other_files
        )
        return application


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomElephantUser
        fields = [
            'username', 'password',
        ]

    def create(self, validated_data):
        user = CustomElephantUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

import pytest
from django.utils import timezone
from backend.models import (
    Brand, CarModel,
    Problems, Engine,
    Chassis, Music,
    Other, Insurance,
    Photo, Car, Price
)


@pytest.mark.django_db
def test_brand_model():
    brand = Brand.objects.create(name='Toyota')
    assert brand.id is not None
    assert brand.name == 'Toyota'
    assert str(brand) == 'Toyota'


@pytest.mark.django_db
def test_car_model_model():
    car_model = CarModel.objects.create(name='Corolla')
    assert car_model.id is not None
    assert car_model.name == 'Corolla'
    assert str(car_model) == 'Corolla'


@pytest.mark.django_db
def test_problems_model():
    problem = Problems.objects.create(name='Scratched paint')
    assert problem.id is not None
    assert problem.name == 'Scratched paint'
    assert not problem.is_solved
    assert problem.created_at is not None
    assert problem.solved_at is None
    assert str(problem) == 'Scratched paint'
    problem.solve()
    assert problem.is_solved
    assert problem.solved_at is not None


@pytest.mark.django_db
def test_engine_model():
    engine = Engine.objects.create(
        engine_type=1.8,
        capacity=1800,
        fuel='petrol',
        tank=50,
        fuel_consumption=7
    )
    assert engine.id is not None
    assert engine.engine_type == 1.8
    assert engine.capacity == 1800
    assert engine.fuel == 'petrol'
    assert engine.tank == 50
    assert engine.fuel_consumption == 7


@pytest.mark.django_db
def test_chassis_model():
    chassis = Chassis.objects.create(
        transmission='automatic',
        drive='front_wheel',
        chassis_abs=True,
        chassis_ebd=True,
        chassis_esp=True
    )
    assert chassis.id is not None
    assert chassis.transmission == 'automatic'
    assert chassis.drive == 'front_wheel'
    assert chassis.chassis_abs
    assert chassis.chassis_ebd
    assert chassis.chassis_esp


@pytest.mark.django_db
def test_music_model():
    music = Music.objects.create(
        radio=True,
        audio_cd=True,
        audio_mp3=True,
        audio_usb=True,
        audio_aux=True,
        audio_bluetooth=True
    )
    assert music.id is not None
    assert music.radio
    assert music.audio_cd
    assert music.audio_mp3
    assert music.audio_usb
    assert music.audio_aux
    assert music.audio_bluetooth


@pytest.mark.django_db
def test_other_model():
    other = Other.objects.create(
        category_drivers_license='B',
        seats=5,
        doors=4,
        air_conditioner=1,
        interior='leather',
        roof='sunroof',
        powered_window=1,
        airbags=6,
        side_wheel='left',
        cruise_control=True,
        rear_view_camera=True,
        parking_assist=True
    )
    assert other.id is not None
    assert other.category_drivers_license == 'B'
    assert other.seats == 5
    assert other.doors == 4
    assert other.air_conditioner == 1
    assert other.interior == 'leather'
    assert other.roof == 'sunroof'
    assert other.powered_window == 1
    assert other.airbags == 6
    assert other.side_wheel == 'left'
    assert other.cruise_control
    assert other.rear_view_camera
    assert other.parking_assist


@pytest.mark.django_db
def test_insurance_model():
    insurance = Insurance.objects.create(
        number='123456',
        is_expired=False,
        expired_at=timezone.now() + timezone.timedelta(days=365)
    )
    assert insurance.id is not None
    assert insurance.number == '123456'
    assert not insurance.is_expired
    assert insurance.expired_at is not None
    assert str(insurance) == '123456'


@pytest.mark.django_db
def test_photo_model():
    photo = Photo.objects.create(car_image='path/to/image.jpg')
    assert photo.id is not None
    assert photo.car_image == 'path/to/image.jpg'


@pytest.mark.django_db
def test_car_model():
    brand = Brand.objects.create(name='Toyota')
    model = CarModel.objects.create(name='Corolla')
    engine = Engine.objects.create(
        engine_type=1.8,
        capacity=1800,
        fuel='petrol',
        tank=50,
        fuel_consumption=7
    )
    chassis = Chassis.objects.create(
        transmission='automatic',
        drive='front_wheel',
        chassis_abs=True,
        chassis_ebd=True,
        chassis_esp=True
    )
    music = Music.objects.create(
        radio=True,
        audio_cd=True,
        audio_mp3=True,
        audio_usb=True,
        audio_aux=True,
        audio_bluetooth=True
    )
    other = Other.objects.create(
        category_drivers_license='B',
        seats=5,
        doors=4,
        air_conditioner=1,
        interior='leather',
        roof='sunroof',
        powered_window=1,
        airbags=6,
        side_wheel='left',
        cruise_control=True,
        rear_view_camera=True,
        parking_assist=True
    )
    insurance = Insurance.objects.create(
        number='123456',
        is_expired=False,
        expired_at=timezone.now() + timezone.timedelta(days=365)
    )
    photo = Photo.objects.create(car_image='path/to/image.jpg')
    car = Car.objects.create(
        brand=brand,
        model=model,
        engine=engine,
        chassis=chassis,
        music=music,
        other=other,
        insurance=insurance,
        number='ABC123',
        year_manufactured=2020,
        body_type='sedan',
        deposit=1000,
        color='red'
    )
    car.photos.add(photo)
    assert car.id is not None
    assert car.brand == brand
    assert car.model == model
    assert car.engine == engine
    assert car.chassis == chassis
    assert car.music == music
    assert car.other == other
    assert car.insurance == insurance
    assert car.number == 'ABC123'
    assert car.year_manufactured == 2020
    assert car.body_type == 'sedan'
    assert car.deposit == 1000
    assert car.color == 'red'
    assert car.created_at is not None
    assert car.updated_at is not None
    assert photo in car.photos.all()


@pytest.mark.django_db
def test_price_model():
    car = Car.objects.create(
        brand=Brand.objects.create(name='Toyota'),
        model=CarModel.objects.create(name='Corolla'),
        engine=Engine.objects.create(
            engine_type=1.8,
            capacity=1800,
            fuel='petrol',
            tank=50,
            fuel_consumption=7
        ),
        chassis=Chassis.objects.create(
            transmission='automatic',
            drive='front_wheel',
            chassis_abs=True,
            chassis_ebd=True,
            chassis_esp=True
        ),
        music=Music.objects.create(
            radio=True,
            audio_cd=True,
            audio_mp3=True,
            audio_usb=True,
            audio_aux=True,
            audio_bluetooth=True
        ),
        other=Other.objects.create(
            category_drivers_license='B',
            seats=5,
            doors=4,
            air_conditioner=1,
            interior='leather',
            roof='sunroof',
            powered_window=1,
            airbags=6,
            side_wheel='left',
            cruise_control=True,
            rear_view_camera=True,
            parking_assist=True
        ),
        insurance=Insurance.objects.create(
            number='123456',
            is_expired=False,
            expired_at=timezone.now() + timezone.timedelta(days=365)
        ),
        number='ABC123',
        year_manufactured=2020,
        body_type='sedan',
        deposit=1000,
        color='red'
    )
    price = Price.objects.create(
        car_price=car,
        winter_price=100.00,
        spring_price=120.00,
        summer_price=150.00,
        autumn_price=110.00,
        currency='USD'
    )
    assert price.id is not None
    assert price.car_price == car
    assert price.winter_price == 100.00
    assert price.spring_price == 120.00
    assert price.summer_price == 150.00
    assert price.autumn_price == 110.00
    assert price.currency == 'USD'

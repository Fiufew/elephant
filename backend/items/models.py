from random import randint

from django.db import models, transaction
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from .validators import validate_manufactured_year
from .const import (
    CURRENCY_CHOICES, MAX_PROBLEM_LEN,
    FUEL_CHOICES, TRANSMISSION_CHOICES,
    DRIVE_CHOICES, CATEGORY_DRIVES_LICENSE_CHOICES,
    AIR_CONDITIONER_CHOICES, INTERIOR_CHOICES,
    ROOF_CHOICES, POWERED_WINDOW_CHOICES,
    SIDE_WHEEL_CHOICES, COLOR_CHOICES,
    BODY_TYPE_CHOICES, AGGREGATOR_CHOICES
    )


class Brand(models.Model):
    name = models.CharField(
        max_length=128
    )

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(
        max_length=128
    )

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'Model'
        verbose_name_plural = 'Models'

    def __str__(self):
        return self.name


class Problem(models.Model):
    name = models.TextField(
        null=True,
        blank=True
    )
    is_solved = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    solved_at = models.DateTimeField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'Problem'
        verbose_name_plural = 'Problems'

    def save(self, *args, **kwargs):
        if len(self.name) > MAX_PROBLEM_LEN:
            raise ValidationError('Text is too long')
        super().save(*args, **kwargs)

    def solve(self):
        if self.is_solved:
            return
        with transaction.atomic():
            self.is_solved = True
            self.solved_at = timezone.now()
            self.save()

    def __str__(self):
        return self.name


class Engine(models.Model):
    engine_type = models.DecimalField(
        max_digits=3,
        decimal_places=1
    )
    capacity = models.PositiveIntegerField()
    fuel = models.CharField(
        max_length=64,
        choices=FUEL_CHOICES
    )
    tank = models.PositiveIntegerField()
    fuel_consumption = models.PositiveIntegerField()

    class Meta:
        ordering = ['engine_type']
        verbose_name = 'Engine'
        verbose_name_plural = 'Engines'


class Chassis(models.Model):
    transmission = models.CharField(
        max_length=64,
        choices=TRANSMISSION_CHOICES
    )
    drive = models.CharField(
        max_length=64,
        choices=DRIVE_CHOICES
    )
    chassis_abs = models.BooleanField(
        default=False
    )
    chassis_ebd = models.BooleanField(
        default=False
    )
    chassis_esp = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ['transmission']
        verbose_name = 'Chassis'
        verbose_name_plural = 'Chassis'


class Music(models.Model):
    radio = models.BooleanField(
        default=False
    )
    audio_cd = models.BooleanField(
        default=False
    )
    audio_mp3 = models.BooleanField(
        default=False
    )
    audio_usb = models.BooleanField(
        default=False
    )
    audio_aux = models.BooleanField(
        default=False
    )
    audio_bluetooth = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ['radio']
        verbose_name = 'Music'
        verbose_name_plural = 'Musics'


class Other(models.Model):
    category_drivers_license = models.CharField(
        max_length=64,
        choices=CATEGORY_DRIVES_LICENSE_CHOICES
    )
    seats = models.PositiveIntegerField()
    doors = models.PositiveIntegerField()
    air_conditioner = models.CharField(
        max_length=128,
        choices=AIR_CONDITIONER_CHOICES
    )
    interior = models.CharField(
        max_length=128,
        choices=INTERIOR_CHOICES
    )
    roof = models.CharField(
        max_length=128,
        choices=ROOF_CHOICES
    )
    powered_window = models.IntegerField(
        choices=POWERED_WINDOW_CHOICES
    )
    airbags = models.PositiveIntegerField()
    side_wheel = models.CharField(
        max_length=64,
        choices=SIDE_WHEEL_CHOICES
    )
    cruise_control = models.BooleanField(
        default=False
    )
    rear_view_camera = models.BooleanField(
        default=False
    )
    parking_assist = models.BooleanField(
        default=False
    )


class Insurance(models.Model):
    number = models.CharField(
        max_length=128
    )
    is_expired = models.BooleanField(
        default=False
    )
    expired_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.number


class Photo(models.Model):
    car_image = models.ImageField(
        null=True,
        blank=True,
        upload_to="files/documents_and_other/"
    )


class Car(models.Model):
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='cars',
        verbose_name='Brand'
    )
    model = models.ForeignKey(
        CarModel,
        on_delete=models.CASCADE,
        related_name='cars',
        verbose_name='Model'
    )
    insurance = models.ForeignKey(
        Insurance,
        on_delete=models.CASCADE,
        related_name='car_insurance',
        verbose_name='Car'
    )
    engine = models.OneToOneField(
        Engine,
        on_delete=models.CASCADE,
        related_name='car',
        verbose_name='Engine'
    )
    chassis = models.OneToOneField(
        Chassis,
        on_delete=models.CASCADE,
        related_name='car',
        verbose_name='Chassis'
    )
    music = models.OneToOneField(
        Music,
        on_delete=models.CASCADE,
        related_name='car',
        verbose_name='Music'
    )
    other = models.OneToOneField(
        Other,
        on_delete=models.CASCADE,
        related_name='car',
        verbose_name='Other Features'
    )
    photos = models.ManyToManyField(
        Photo,
        related_name='cars',
        verbose_name='Photos',
        blank=True
    )
    problems = models.ManyToManyField(
        Problem,
        related_name='cars',
        verbose_name='Problems',
        blank=True
    )
    number = models.CharField(
        max_length=64,
    )
    year_manufactured = models.PositiveIntegerField(
        validators=[
            validate_manufactured_year
        ],
        verbose_name='Year Manufactured'
    )
    body_type = models.CharField(
        max_length=128,
        choices=BODY_TYPE_CHOICES
    )
    deposit = models.PositiveIntegerField()
    color = models.CharField(
        max_length=64,
        choices=COLOR_CHOICES
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )

    class Meta:
        ordering = ['brand', 'model']
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'
        indexes = [
            models.Index(
                fields=['year_manufactured'],
                name='year_manufactured_idx'),
            models.Index(fields=['brand', 'model'], name='brand_model_idx'),
            models.Index(fields=['-created_at'], name='created_at_idx'),
            models.Index(fields=['-updated_at'], name='updated_at_idx'),
        ]

    def __str__(self):
        return f'{self.brand.name} {self.model.name}'


class Price(models.Model):
    car_price = models.OneToOneField(
        Car,
        on_delete=models.CASCADE,
        related_name='price',
        null=True,
        blank=True
        )
    winter_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
        )
    spring_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
        )
    summer_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
        )
    autumn_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
        )
    currency = models.CharField(
        max_length=10,
        null=True,
        choices=CURRENCY_CHOICES,
        )


class Application(models.Model):
    num = models.IntegerField(
        unique=True,
        null=True,
        blank=True
    )
    aggregator = models.CharField(
        max_length=128,
        choices=AGGREGATOR_CHOICES
    )
    date = models.DateField()
    auto = models.ForeignKey(
        'Car',
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Car'
    )
    location_delivery = models.CharField(
        max_length=256
    )
    location_return = models.CharField(
        max_length=256
    )
    name = models.CharField(
        max_length=256
    )
    contacts = models.CharField(
        max_length=64
    )
    deposit_in_hand = models.IntegerField()
    currency = models.CharField(
        choices=CURRENCY_CHOICES,
        max_length=256
    )
    price = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.num:
            while True:
                new_num = randint(100000, 999999)
                if not Application.objects.filter(num=new_num).exists():
                    self.num = new_num
                    break
        super().save(*args, **kwargs)


class Date(models.Model):
    application = models.OneToOneField(
        'Application',
        on_delete=models.CASCADE,
        related_name='rental_dates'
    )
    date_delivery = models.DateField()
    date_return = models.DateField()


class Misc(models.Model):
    contract = models.FileField(
        upload_to='contracts/',
        null=True,
        blank=True)
    vaucher = models.FileField(
        upload_to='vauchers/',
        null=True,
        blank=True)
    video = models.FileField(
        upload_to='videos/',
        null=True,
        blank=True)
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='misc_files',
    )

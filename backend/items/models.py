from random import randint

from django.db import models, transaction
from django.utils import timezone
from django.core.exceptions import ValidationError

from .validators import validate_manufactured_year
from .path_file import applications_path, bluebook_upload_path
from .const import (
    MAX_PROBLEM_LEN, FUEL_CHOICES, TRANSMISSION_CHOICES,
    DRIVE_CHOICES, CATEGORY_DRIVES_LICENSE_CHOICES, AIR_CONDITIONER_CHOICES,
    INTERIOR_CHOICES, ROOF_CHOICES, POWERED_WINDOW_CHOICES,
    SIDE_WHEEL_CHOICES, COLOR_CHOICES, BODY_TYPE_CHOICES,
    AGREGATOR_CHOICES, STATUS_CHOICES, CONTACT_CHOICES,
    BRAND_CHOICES, DOORS_CHOICES, AIRBAGS_CHOICES,
    CURRENCY_CHOICES, BABY_SEAT_CHOICES, ANOTHER_REGIONS_CHOICES,
    COMPLEX_INSURANCE_CHOICES,
    )


class CarBrand(models.Model):
    name = models.CharField(
        choices=BRAND_CHOICES,
        max_length=64,
    )

    class Meta:
        ordering = [
            'name'
        ]
        indexes = [
            models.Index(
                fields=['name']
            )
        ]
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(
        max_length=64,
    )

    class Meta:
        ordering = [
            'name'
        ]
        indexes = [
            models.Index(
                fields=['name']
            )
        ]
        verbose_name = 'Model'
        verbose_name_plural = 'Models'

    def __str__(self):
        return self.name


class Problem(models.Model):
    name = models.TextField(
        null=True,
        blank=True,
    )
    is_solved = models.BooleanField(
        default=False,
    )
    solved_at = models.DateTimeField(
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = [
            'name'
        ]
        indexes = [
            models.Index(
                fields=['name']
            )
        ]
        verbose_name = 'Problem'
        verbose_name_plural = 'Problems'

    def save(self, *args, **kwargs):
        if self.name and len(self.name) > MAX_PROBLEM_LEN:
            raise ValidationError('Text is too long')
        super().save(*args, **kwargs)

    def solve(self, commit=True):
        if self.is_solved:
            return False
        self.is_solved = True
        self.solved_at = timezone.now()
        if commit:
            with transaction.atomic():
                self.save()
        return True

    def __str__(self):
        return self.name


class Engine(models.Model):
    fuel = models.CharField(
        choices=FUEL_CHOICES,
        max_length=64,
    )
    capacity = models.PositiveIntegerField()
    power = models.PositiveIntegerField()
    tank = models.PositiveIntegerField()
    fuel_consumption = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Engine'
        verbose_name_plural = 'Engines'


class Chassis(models.Model):
    transmission = models.CharField(
        choices=TRANSMISSION_CHOICES,
        max_length=64,
    )
    drive = models.CharField(
        choices=DRIVE_CHOICES,
        max_length=64,
    )
    chassis_abs = models.BooleanField(
        default=False,
    )
    chassis_ebd = models.BooleanField(
        default=False,
    )
    chassis_esp = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = [
            'transmission'
        ]
        verbose_name = 'Chassis'
        verbose_name_plural = 'Chassis'


class Music(models.Model):
    radio = models.BooleanField(
        default=False,
    )
    audio_cd = models.BooleanField(
        default=False,
    )
    audio_mp3 = models.BooleanField(
        default=False,
    )
    audio_usb = models.BooleanField(
        default=False,
    )
    audio_aux = models.BooleanField(
        default=False,
    )
    audio_bluetooth = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = 'Music'
        verbose_name_plural = 'Musics'


class Other(models.Model):
    category_drivers_license = models.CharField(
        choices=CATEGORY_DRIVES_LICENSE_CHOICES,
        max_length=64,
    )
    seats = models.PositiveIntegerField()
    doors = models.IntegerField(
        choices=DOORS_CHOICES,
    )
    air_conditioner = models.CharField(
        choices=AIR_CONDITIONER_CHOICES,
        max_length=64,
    )
    interior = models.CharField(
        choices=INTERIOR_CHOICES,
        max_length=64,
    )
    roof = models.CharField(
        choices=ROOF_CHOICES,
        max_length=64,
    )
    powered_window = models.IntegerField(
        choices=POWERED_WINDOW_CHOICES,
    )
    airbags = models.IntegerField(
        choices=AIRBAGS_CHOICES,
    )
    side_wheel = models.CharField(
        choices=SIDE_WHEEL_CHOICES,
        max_length=64,
    )
    cruise_control = models.BooleanField(
        default=False,
    )
    rear_view_camera = models.BooleanField(
        default=False,
    )
    parking_assist = models.BooleanField(
        default=False,
    )


class Act(models.Model):
    car = models.OneToOneField(
        'Car',
        on_delete=models.CASCADE,
        related_name='car_act'
    )
    is_expired = models.BooleanField(
        default=False,
    )
    expired_at = models.DateField(
        null=True,
    )


class FirstClass(models.Model):
    car = models.OneToOneField(
        'Car',
        on_delete=models.CASCADE,
        related_name='car_firstclass'
    )
    is_expired = models.BooleanField(
        default=False,
    )
    expired_at = models.DateField(
        null=True,
        blank=True,
    )


class SecondClass(models.Model):
    car = models.OneToOneField(
        'Car',
        on_delete=models.CASCADE,
        related_name='car_secondclass'
    )
    is_expired = models.BooleanField(
        default=False,
    )
    expired_at = models.DateField(
        null=True,
        blank=True,
    )


class Tax(models.Model):
    car = models.OneToOneField(
        'Car',
        on_delete=models.CASCADE,
        related_name='car_tax'
    )
    is_expired = models.BooleanField(
        default=False,
    )
    expired_at = models.DateField(
        null=True,
        blank=True,
    )


class Bluebook(models.Model):
    car = models.OneToOneField(
        'Car',
        on_delete=models.CASCADE,
        related_name='car_bluebook'
    )
    is_expired = models.BooleanField(
        default=False,
    )
    expired_at = models.DateField(
        null=True,
        blank=True,
    )
    bluebook_image = models.ImageField(
        null=True,
        blank=True,
        upload_to=bluebook_upload_path,
    )


class Photo(models.Model):
    car = models.ForeignKey(
        'Car',
        on_delete=models.CASCADE,
        related_name='car_photos',
    )
    car_image = models.ImageField(
        upload_to='car_photos/',
        null=True,
        blank=True,
    )


class Car(models.Model):
    brand = models.ForeignKey(
        CarBrand,
        on_delete=models.CASCADE,
        related_name='cars_brand',
        verbose_name='Brand',
    )
    model = models.ForeignKey(
        CarModel,
        on_delete=models.CASCADE,
        related_name='cars_model',
        verbose_name='Model',
    )
    act = models.ForeignKey(
        Act,
        on_delete=models.CASCADE,
        related_name='car_act',
        verbose_name='act',
        null=True,
        blank=True,
    )
    first_class = models.ForeignKey(
        FirstClass,
        on_delete=models.CASCADE,
        related_name='car_first_class',
        verbose_name='first_class',
        null=True,
        blank=True,
    )
    second_class = models.ForeignKey(
        SecondClass,
        on_delete=models.CASCADE,
        related_name='car_second_class',
        verbose_name='second_class',
        null=True,
        blank=True,
    )
    tax = models.ForeignKey(
        Tax,
        on_delete=models.CASCADE,
        related_name='car_tax',
        verbose_name='tax',
        null=True,
        blank=True,
    )
    bluebook = models.ForeignKey(
        Bluebook,
        on_delete=models.CASCADE,
        related_name='car_bluebook',
        verbose_name='bluebook',
        null=True,
        blank=True,
    )
    engine = models.OneToOneField(
        Engine,
        on_delete=models.CASCADE,
        related_name='car_engine',
        verbose_name='Engine',
    )
    chassis = models.OneToOneField(
        Chassis,
        on_delete=models.CASCADE,
        related_name='car_chassis',
        verbose_name='Chassis',
    )
    music = models.OneToOneField(
        Music,
        on_delete=models.CASCADE,
        related_name='car_music',
        verbose_name='Music',
    )
    other = models.OneToOneField(
        Other,
        on_delete=models.CASCADE,
        related_name='car_other',
        verbose_name='Other Features',
    )
    photos = models.ManyToManyField(
        Photo,
        related_name='cars',
        blank=True,
    )
    problems = models.OneToOneField(
        Problem,
        on_delete=models.CASCADE,
        related_name='cars_problems',
        verbose_name='Problems',
        blank=True,
        null=True,
    )
    number = models.CharField(
        max_length=64,
    )
    year_manufactured = models.PositiveIntegerField(
        validators=[
            validate_manufactured_year
        ],
        verbose_name='Year Manufactured',
    )
    body_type = models.CharField(
        choices=BODY_TYPE_CHOICES,
        max_length=64,
    )
    deposit = models.PositiveIntegerField()
    color = models.CharField(
        choices=COLOR_CHOICES,
        max_length=64,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At',
    )
    pick_season = models.IntegerField(
        null=True,
        blank=True,
    )
    high_season = models.IntegerField(
        null=True,
        blank=True,
    )
    low_season = models.IntegerField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = [
            'brand', 'model'
        ]
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'
        indexes = [
            models.Index(
                fields=['year_manufactured'], name='year_manufactured_idx',
            ),
            models.Index(
                fields=['brand', 'model'], name='brand_model_idx',
            ),
            models.Index(
                fields=['-created_at'], name='created_at_idx',
            ),
            models.Index(
                fields=['-updated_at'], name='updated_at_idx',
            ),
        ]

    def __str__(self):
        return f'{self.brand.name} {self.model.name}'


class Application(models.Model):
    num = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
    )
    agregator = models.CharField(
        choices=AGREGATOR_CHOICES,
        max_length=64,
    )
    auto = models.ForeignKey(
        'Car',
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Car',
    )
    location_delivery = models.CharField(
        max_length=64,
    )
    url_delivery = models.URLField()
    location_return = models.CharField(
        max_length=64,
    )
    url_return = models.URLField()
    client_name = models.CharField(
        max_length=64,
    )
    birthdate = models.DateField(
        blank=True,
        null=True,
    )
    contacts = models.CharField(
        max_length=64,
    )
    contact_type = models.CharField(
        choices=CONTACT_CHOICES,
        max_length=64,
    )
    client_email = models.EmailField(
        blank=True,
        null=True,
    )
    deposit_in_hand = models.IntegerField()
    currency = models.CharField(
        choices=CURRENCY_CHOICES,
        max_length=64,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    rental_dates = models.OneToOneField(
        'Date',
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=64,
        choices=STATUS_CHOICES,
        default='Active',
    )
    baby_seat = models.CharField(
        choices=BABY_SEAT_CHOICES,
        max_length=64,
        default='-',
    )
    another_regions = models.CharField(
        choices=ANOTHER_REGIONS_CHOICES,
        max_length=64,
        default='-',
    )
    complex_insurance = models.CharField(
        choices=COMPLEX_INSURANCE_CHOICES,
        max_length=64,
        default='-',
    )

    def save(self, *args, **kwargs):
        if not self.num:
            while True:
                new_num = randint(100000, 999999)
                if not Application.objects.filter(num=new_num).exists():
                    self.num = new_num
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.num} - {self.client_name}'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'


class Date(models.Model):
    application = models.OneToOneField(
        'Application',
        on_delete=models.CASCADE,
        related_name='rental_date'
    )
    date_delivery = models.DateField()
    date_return = models.DateField()
    number_of_days = models.PositiveIntegerField(default=0)


class Misc(models.Model):
    contract = models.FileField(
        upload_to=applications_path,
        null=True,
        blank=True)
    vaucher = models.FileField(
        upload_to='vauchers/',
        null=True,
        blank=True)
    other_files = models.FileField(
        upload_to=applications_path,
        null=True,
        blank=True)
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='misc_files',
    )

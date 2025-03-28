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
    BODY_TYPE_CHOICES, AGGREGATOR_CHOICES,
    STATUS_CHOICES, CONTACT_CHOICES, BRAND_CHOICES,
    DOORS_CHOICES, AIRBAGS_CHOICES
    )


class CarBrand(models.Model):
    name = models.CharField(  # наименовение бренда авто (сделать выбор)
        max_length=128,
        choices=BRAND_CHOICES
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
    name = models.CharField(  # наименовение модели авто
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
    name = models.TextField(  # наименовение проблемы у авто
        null=True,
        blank=True
    )
    is_solved = models.BooleanField(  # флаг решения или актуальности проблемы, изначально нерешенная
        default=False
    )
    created_at = models.DateTimeField(  # дата создания (автоматически)
        auto_now_add=True
    )
    solved_at = models.DateTimeField(  # дата решения
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

    def save(self, *args, **kwargs):  # ограничение на длину текста проблемы
        if self.name and len(self.name) > MAX_PROBLEM_LEN:
            raise ValidationError('Text is too long')
        super().save(*args, **kwargs)

    def solve(self):  # изменение флага решенности проблемы и сохранение времени при его изменении
        if self.is_solved:
            return
        with transaction.atomic():
            self.is_solved = True
            self.solved_at = timezone.now()
            self.save()

    def __str__(self):
        return self.name


class Engine(models.Model):
    fuel = models.CharField(  # тип топлива
        max_length=64,
        choices=FUEL_CHOICES
    )
    capacity = models.PositiveIntegerField()  # объем двигателя
    power = models.PositiveIntegerField()  # мощность двигателя
    tank = models.PositiveIntegerField()  # объем бака
    fuel_consumption = models.PositiveIntegerField()  # расход л/100

    class Meta:
        verbose_name = 'Engine'
        verbose_name_plural = 'Engines'


class Chassis(models.Model):
    transmission = models.CharField(  # вид трансмиссии
        max_length=64,
        choices=TRANSMISSION_CHOICES
    )
    drive = models.CharField(  # вид привода
        max_length=64,
        choices=DRIVE_CHOICES
    )
    chassis_abs = models.BooleanField(  # наличие абс
        default=False
    )
    chassis_ebd = models.BooleanField(  # наличие ебд
        default=False
    )
    chassis_esp = models.BooleanField(  # наличие есп
        default=False
    )

    class Meta:
        ordering = ['transmission']
        verbose_name = 'Chassis'
        verbose_name_plural = 'Chassis'


class Music(models.Model):
    radio = models.BooleanField(  # наличие радио
        default=False
    )
    audio_cd = models.BooleanField(  # наличие сд
        default=False
    )
    audio_mp3 = models.BooleanField(  # наличие мп3
        default=False
    )
    audio_usb = models.BooleanField(  # наличие наличие юсб
        default=False
    )
    audio_aux = models.BooleanField(  # наличие аукса
        default=False
    )
    audio_bluetooth = models.BooleanField(  # наличие блютуза
        default=False
    )

    class Meta:
        ordering = ['radio']
        verbose_name = 'Music'
        verbose_name_plural = 'Musics'


class Other(models.Model):
    category_drivers_license = models.CharField(  # категория прав для авто
        max_length=64,
        choices=CATEGORY_DRIVES_LICENSE_CHOICES
    )
    seats = models.PositiveIntegerField()
    doors = models.CharField(
        choices=DOORS_CHOICES,
        max_length=255
    ) # количество дверей (сделать выбор)
    air_conditioner = models.CharField(  # тип кондиционирования
        max_length=128,
        choices=AIR_CONDITIONER_CHOICES
    )
    interior = models.CharField(  # тип интерьера
        max_length=128,
        choices=INTERIOR_CHOICES
    )
    roof = models.CharField(  # тип крыши
        max_length=128,
        choices=ROOF_CHOICES
    )
    powered_window = models.CharField(  # количество стеклоподъемников
        choices=POWERED_WINDOW_CHOICES,
        max_length=255
    )
    airbags = models.CharField(
        choices=AIRBAGS_CHOICES,
        max_length=255
    )  # количество подушек безопасности (сделать выбор)
    side_wheel = models.CharField(  # сторона руля
        max_length=64,
        choices=SIDE_WHEEL_CHOICES
    )
    cruise_control = models.BooleanField(  # наличие круиз контроля
        default=False
    )
    rear_view_camera = models.BooleanField(  # наличие камеры заднего вида
        default=False
    )
    parking_assist = models.BooleanField(  # наличие парктроника
        default=False
    )


class ACT(models.Model):
    name = models.CharField(  # название страховки
        max_length=128
    )
    is_expired = models.BooleanField(  # истекла ли, false, значит нет, true - да
        default=False
    )
    expired_at = models.DateTimeField(  # страховка действительна до этой даты
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class FirstClass(models.Model):
    name = models.CharField(  # название страховки
        max_length=128
    )
    is_expired = models.BooleanField(  # истекла ли, false, значит нет, true - да
        default=False
    )
    expired_at = models.DateTimeField(  # страховка действительна до этой даты
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class SecondClass(models.Model):
    name = models.CharField(  # название страховки
        max_length=128
    )
    is_expired = models.BooleanField(  # истекла ли, false, значит нет, true - да
        default=False
    )
    expired_at = models.DateTimeField(  # страховка действительна до этой даты
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Tax(models.Model):
    name = models.CharField(  # название страховки
        max_length=128
    )
    is_expired = models.BooleanField(  # истекла ли, false, значит нет, true - да
        default=False
    )
    expired_at = models.DateTimeField(  # страховка действительна до этой даты
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Bluebook(models.Model):
    name = models.CharField(  # название страховки
        max_length=128
    )
    is_expired = models.BooleanField(  # истекла ли, false, значит нет, true - да
        default=False
    )
    expired_at = models.DateTimeField(  # страховка действительна до этой даты
        null=True,
        blank=True
    )
    bluebook_image = models.ImageField(  # фотография авто
        null=True,
        blank=True,
        upload_to="files/bluebook/"
    )

    def __str__(self):
        return self.name


class Photo(models.Model):
    car_image = models.ImageField(  # фотография авто
        null=True,
        blank=True,
        upload_to="files/documents_and_other/"
    )


class Price(models.Model):
    pick_season = models.IntegerField(
        null=True,
        blank=True
    )
    high_season = models.IntegerField(
        null=True,
        blank=True
    )
    low_season = models.IntegerField(
        null=True,
        blank=True
    )
    currency = models.CharField(  # тип валюты? нужен ли и как испольлзовать вопрос
        max_length=10,
        null=True,
        choices=CURRENCY_CHOICES,
        )


class Car(models.Model):
    brand = models.ForeignKey(  # название бренда сторонний класс
        CarBrand,
        on_delete=models.CASCADE,
        related_name='cars',
        verbose_name='Brand'
    )
    model = models.ForeignKey(  # название модели сторонний класс
        CarModel,
        on_delete=models.CASCADE,
        related_name='cars_model',
        verbose_name='Model'
    )
    act = models.ForeignKey(  # информация о страховке, сторонний класс
        ACT,
        on_delete=models.CASCADE,
        related_name='car_act',
        verbose_name='act',
        null=True,
        blank=True
    )
    first_class = models.ForeignKey( # информация о страховке, сторонний класс
        FirstClass,
        on_delete=models.CASCADE,
        related_name='car_first_class',
        verbose_name='first_class',
        null=True,
        blank=True
    )
    second_class = models.ForeignKey(  # информация о страховке, сторонний класс
        SecondClass,
        on_delete=models.CASCADE,
        related_name='car_second_class',
        verbose_name='second_class',
        null=True,
        blank=True
    )
    tax = models.ForeignKey(  #  информация о страховке, сторонний класс
        Tax,
        on_delete=models.CASCADE,
        related_name='car_tax',
        verbose_name='tax',
        null=True,
        blank=True
    )
    bluebook = models.ForeignKey(  # информация о страховке, сторонний класс
        Bluebook,
        on_delete=models.CASCADE,
        related_name='car_bluebook',
        verbose_name='bluebook',
        null=True,
        blank=True
    )
    engine = models.OneToOneField(  # информация о двигателе, сторонний класс
        Engine,
        on_delete=models.CASCADE,
        related_name='car_engine',
        verbose_name='Engine'
    )
    chassis = models.OneToOneField(  # информация о шасси, сторонний класс
        Chassis,
        on_delete=models.CASCADE,
        related_name='car_chassis',
        verbose_name='Chassis'
    )
    music = models.OneToOneField(  # информация о муз.возможностях, сторонний класс
        Music,
        on_delete=models.CASCADE,
        related_name='car_music',
        verbose_name='Music'
    )
    other = models.OneToOneField(  # информация о другом сторонний класс
        Other,
        on_delete=models.CASCADE,
        related_name='car_other',
        verbose_name='Other Features'
    )
    photos = models.OneToOneField(  # фотографии автомобилей сторонний класс
        Photo,
        on_delete=models.CASCADE,
        related_name='cars_photos',
        verbose_name='Photos',
        blank=True,
        null=True
    )
    problems = models.OneToOneField(  # проблемы с автомобилем сторонний класс
        Problem,
        on_delete=models.CASCADE,
        related_name='cars_problems',
        verbose_name='Problems',
        blank=True,
        null=True
    )
    number = models.CharField(  # гос номер
        max_length=64,
    )
    year_manufactured = models.PositiveIntegerField(  # год выпуска авто
        validators=[
            validate_manufactured_year
        ],
        verbose_name='Year Manufactured'
    )
    body_type = models.CharField(  #  тип кузова
        max_length=128,
        choices=BODY_TYPE_CHOICES
    )
    deposit = models.PositiveIntegerField()  # депозит для авто
    color = models.CharField(  # цвет автомобиля
        max_length=64,
        choices=COLOR_CHOICES
    )
    created_at = models.DateTimeField(  # дата и время создания в бд данного авто
        auto_now_add=True,
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(  #  дата и время изменения записи об авто в бд
        auto_now=True,
        verbose_name='Updated At'
    )
    price = models.OneToOneField(
        Price,
        on_delete=models.CASCADE,
        related_name='car',
        verbose_name='Price',
        blank=True,
        null=True
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


class Application(models.Model):
    num = models.IntegerField(  # номер заявки
        unique=True,
        null=True,
        blank=True
    )
    aggregator = models.CharField(  # с какого агрегатора заявка
        max_length=128,
        choices=AGGREGATOR_CHOICES
    )
    auto = models.ForeignKey(  # какое авто фигурирует в заявке
        'Car',
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Car'
    )
    location_delivery = models.CharField(  # локация доставки авто
        max_length=256
    )
    location_return = models.CharField(  # локация возврата авто
        max_length=256
    )
    client_name = models.CharField(  # имя клиента
        max_length=256
    )
    birthdate = models.DateField(  # дата рождения клиента
        blank=True,
        null=True
    )
    contacts = models.CharField(  # номер телефона
        max_length=64
    )
    contact_type = models.CharField(  # тип связи с клиентом
        max_length=64,
        choices=CONTACT_CHOICES,
    )
    client_email = models.EmailField(  # почта клиента
        blank=True,
        null=True
    )
    deposit_in_hand = models.IntegerField()  # депозит на руки
    currency = models.CharField(  # тип валюты
        choices=CURRENCY_CHOICES,
        max_length=256
    )
    price = models.IntegerField()  # цена
    status = models.CharField(  # статус заявки
        max_length=128,
        choices=STATUS_CHOICES,
        default='Active'
    )

    def save(self, *args, **kwargs):  # генерация номера
        if not self.num:
            while True:
                new_num = randint(100000, 999999)
                if not Application.objects.filter(num=new_num).exists():
                    self.num = new_num
                    break
        super().save(*args, **kwargs)


class Date(models.Model):
    application = models.OneToOneField(  # инфо о заявке
        'Application',
        on_delete=models.CASCADE,
        related_name='rental_dates'
    )
    date_delivery = models.DateField()  # дата доставки
    date_return = models.DateField()  # дата возврата


class Misc(models.Model):
    contract = models.FileField(  # контракт
        upload_to='contracts/',
        null=True,
        blank=True)
    vaucher = models.FileField(  # ваучер
        upload_to='vauchers/',
        null=True,
        blank=True)
    other_files = models.FileField(  # ваучер
        upload_to='other_files/',
        null=True,
        blank=True)
    application = models.ForeignKey(  # файлы у заявки
        Application,
        on_delete=models.CASCADE,
        related_name='misc_files',
    )

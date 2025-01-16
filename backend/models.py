from django.db import models
from django.utils import timezone

from autoslug import AutoSlugField


class Category(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name


class Investor(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'Investor'
        verbose_name_plural = 'Investors'

    def __str__(self):
        return self.name


class Insurance(models.Model):
    symbol = models.CharField(max_length=128)
    start_date = models.DateTimeField()
    expired_date = models.DateTimeField()

    def check_expiration(self):
        return self.expired_date < self.start_date

    class Meta:
        ordering = ['symbol']
        indexes = [
            models.Index(fields=['symbol'])
        ]
        verbose_name = 'insurance'
        verbose_name_plural = 'insurances'


class Model(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'Model'
        verbose_name_plural = 'Models'

    def __str__(self):
        return self.name


class CarManager(models.Manager):
    def available_cars(self):
        return self.filter(is_availaible=True)


class Car(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='categories',
                                 on_delete=models.CASCADE)
    color = models.ForeignKey(Color,
                              related_name='colors',
                              on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,
                              related_name='brands_in_car',
                              on_delete=models.CASCADE)
    model = models.ForeignKey(Model,
                              related_name='models_in_car',
                              on_delete=models.CASCADE)
    investor = models.ForeignKey(Investor,
                                 related_name='investors',
                                 on_delete=models.CASCADE)
    insurance = models.ForeignKey(Insurance,
                                  related_name='car_insurance',
                                  on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='model', unique=True)
    car_name = models.CharField(max_length=255, blank=True, null=True)
    year_manufactored = models.IntegerField(null=True)
    license_plate = models.CharField(max_length=20, null=True)
    is_availaible = models.BooleanField(default=False)
    image = models.ImageField(blank=True, upload_to='cars/%Y/%m/%d')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CarManager()

    def mark_as_rented(self):
        self.is_availaible = True
        self.save()

    def save(self, *args, **kwargs):
        self.car_name = f"{self.brand}: {self.model}"
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['brand']
        indexes = [
            models.Index(fields=['car_name']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_availaible']),
        ]
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'

    def __str__(self):
        return f'{self.brand}: {self.model}'


class Price(models.Model):
    car_price = models.OneToOneField(Car, on_delete=models.CASCADE,
                                     related_name='price')
    winter_price = models.DecimalField(max_digits=10, decimal_places=2)
    spring_price = models.DecimalField(max_digits=10, decimal_places=2)
    summer_price = models.DecimalField(max_digits=10, decimal_places=2)
    autumn_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, null=True)

    class Meta:
        verbose_name = 'Price'
        verbose_name_plural = 'Prices'

    def __str__(self):
        return 'Актуальная цена'


class Application(models.Model):
    car = models.ForeignKey(Car, related_name='booking_requests',
                            on_delete=models.CASCADE)
    price = models.ForeignKey(Price, related_name='booking_requests_price',
                              on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=512)
    dropoff_location = models.CharField(max_length=512)
    pickup_time = models.DateTimeField()
    dropoff_time = models.DateTimeField()
    renter_name = models.CharField(max_length=128)
    renter_phone = models.CharField(max_length=32)
    renter_email = models.EmailField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    vaucher = ...
    contract = ...

    def check_expiration(self):
        return self.dropoff_time < timezone.now()

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'

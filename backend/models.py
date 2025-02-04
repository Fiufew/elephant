from django.db import models
from django.utils import timezone

from autoslug import AutoSlugField

from .utils import other_files_path_for_application, car_image_upload_to


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
    symbol = models.CharField(max_length=128, null=True)
    start_date = models.DateTimeField()
    expired_date = models.DateTimeField()

    def check_expiration(self):
        return self.expired_date < self.start_date

    def __str__(self):
        return self.symbol

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
    category = models.ForeignKey(
        Category,
        related_name='categories',
        on_delete=models.CASCADE)
    color = models.ForeignKey(
        Color,
        related_name='colors',
        on_delete=models.CASCADE)
    brand = models.ForeignKey(
        Brand,
        related_name='brands_in_car',
        on_delete=models.CASCADE)
    model = models.ForeignKey(
        Model,
        related_name='models_in_car',
        on_delete=models.CASCADE)
    investor = models.ForeignKey(
        Investor,
        related_name='investors',
        on_delete=models.CASCADE)
    insurance = models.ForeignKey(
        Insurance,
        related_name='car_insurance',
        on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='model', unique=True)
    car_name = models.CharField(max_length=255, blank=True, null=True)
    year_manufactored = models.IntegerField(null=True)
    license_plate = models.CharField(max_length=20, null=True)
    is_availaible = models.BooleanField(default=False)
    image = models.ImageField(blank=True, upload_to=car_image_upload_to)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    winter_price = models.DecimalField(max_digits=10, decimal_places=2)
    spring_price = models.DecimalField(max_digits=10, decimal_places=2)
    summer_price = models.DecimalField(max_digits=10, decimal_places=2)
    autumn_price = models.DecimalField(max_digits=10, decimal_places=2)

    objects = CarManager()

    def mark_as_rented(self):
        self.is_availaible = True
        self.save()

    def save(self, *args, **kwargs):
        self.car_name = f"{self.brand} {self.model}"
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

class Application(models.Model):

    CANCELED = 'canceled'
    EXPIRED = 'expired'
    ACTIVE = 'active'

    STATUS_CHOICES = [
        (CANCELED, 'Canceled'),
        (EXPIRED, 'Expired'),
        (ACTIVE, 'Active'),
    ]

    AGGREGATOR_CHOICES = [
        ('aggregator1', 'Aggregator 1'),
        ('aggregator2', 'Aggregator 2'),
        ('aggregator3', 'Aggregator 3'),
    ]

    car = models.ForeignKey(
        Car, related_name='booking_requests',
        on_delete=models.CASCADE)
    price = models.IntegerField(null=True, blank=True)
    pickup_location = models.CharField(max_length=512)
    dropoff_location = models.CharField(max_length=512)
    pickup_time = models.DateTimeField()
    dropoff_time = models.DateTimeField()
    renter_name = models.CharField(max_length=128)
    renter_phone = models.CharField(max_length=32)
    renter_email = models.EmailField(null=True, blank=True)
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES,
        blank=True, default=ACTIVE)
    application_preparer = models.CharField(max_length=64, null=True)
    aggregator_id = models.IntegerField(null=True, blank=True)
    aggregator = models.CharField(
        max_length=32, choices=AGGREGATOR_CHOICES,
        null=True, blank=True)
    comment = models.TextField(blank=True, null=True)
    contract = models.FileField(
        upload_to='contract_dir', null=True, blank=True)
    vaucher = models.FileField(
        upload_to='vaucher_dir', null=True, blank=True)

    def check_expiration(self):
        return self.dropoff_time < timezone.now()

    def change_status(self, new_status):
        if new_status in [self.CANCELED, self.EXPIRED, self.ACTIVE]:
            self.status = new_status
            self.save()
        else:
            raise ValueError(f"Invalid status: {new_status}")

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'


class Problem(models.Model):
    car_problem = models.ForeignKey(
        Car, related_name='problem_car',
        on_delete=models.CASCADE,
        null=True)
    issue = models.TextField()
    is_solved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    solved_at = models.DateTimeField(blank=True, null=True)

    def solve_problem(self):
        self.is_solved = True
        self.solved_at = timezone.now()
        self.save()

    class Meta:
        verbose_name = 'Problem'
        verbose_name_plural = 'Problems'


class Files(models.Model):
    application = models.ForeignKey(
        Application, related_name='files', on_delete=models.CASCADE)
    files_application = models.FileField(
        upload_to=other_files_path_for_application, null=True, blank=True)

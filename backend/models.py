from django.db import models
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
    is_booked = models.BooleanField(default=False)
    insurance = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    state_number = models.CharField(max_length=63)
    slug = AutoSlugField(populate_from='model', unique=True)
    photo = models.ImageField(blank=True, upload_to='cars/%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['brand']),
            models.Index(fields=['-created_at']),
        ]
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'

    def __str__(self):
        return f'{self.brand}: {self.model}'


class Price(models.Model):
    car_price = models.OneToOneField(Car,
                                     on_delete=models.CASCADE,
                                     related_name='price')
    season_one = models.DecimalField(max_digits=10, decimal_places=2)
    season_two = models.DecimalField(max_digits=10, decimal_places=2)
    season_three = models.DecimalField(max_digits=10, decimal_places=2)
    season_four = models.DecimalField(max_digits=10, decimal_places=2)  # добавить поля для количества дней
    season_one_upto7 = models.DecimalField(max_digits=10, decimal_places=2)
    season_two_upto7 = models.DecimalField(max_digits=10, decimal_places=2)
    season_three_upto7 = models.DecimalField(max_digits=10, decimal_places=2)
    season_four_upto7 = models.DecimalField(max_digits=10, decimal_places=2)
    season_one_upto14 = models.DecimalField(max_digits=10, decimal_places=2)
    season_two_upto14 = models.DecimalField(max_digits=10, decimal_places=2)
    season_three_upto14 = models.DecimalField(max_digits=10, decimal_places=2)
    season_four_upto14 = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Price'
        verbose_name_plural = 'Prices'

    def __str__(self):
        return 'Актуальная цена'


class Bid(models.Model):
    CONTACT_CHOICES = [
        ('telegram', 'Telegram'),
        ('whatsapp', 'WhatsApp'),
        ('viber', 'Viber'),
    ]
    car = models.ForeignKey(Car, related_name='booking_requests',
                            on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=511)
    dropoff_location = models.CharField(max_length=511)
    pickup_time = models.DateTimeField()
    dropoff_time = models.DateTimeField()
    renter_name = models.CharField(max_length=255)
    renter_birthdate = models.DateField()
    renter_phone = models.CharField(max_length=20)
    renter_email = models.EmailField()
    contact_method = models.CharField(max_length=10, choices=CONTACT_CHOICES)
    comment = models.TextField(blank=True, null=True)
    bid_preparer = models.CharField(max_length=127)

    class Meta:
        verbose_name = 'Bid'
        verbose_name_plural = 'Bids'

    def __str__(self):
        return f'Bid for {self.car.brand.name} {self.car.model.name} by {self.renter_name}'

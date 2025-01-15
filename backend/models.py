from django.db import models


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
    brand = models.ForeignKey(Brand,
                              related_name='brands',
                              on_delete=models.CASCADE)
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

    class Meta:
        ordering = ['brand']
        indexes = [
            models.Index(fields=['brand']),
            models.Index(fields=['-created_at']),
        ]
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'

    def __str__(self):
        return f'{self.brand}: {self.model}'


class Price(models.Model):
    car_price = models.OneToOneField(Car, on_delete=models.CASCADE,
                                     related_name='price')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)

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

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'

from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255)
    registration_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    date_added = models.DateTimeField(default=timezone.now)

    # Добавляем новое поле для хранения фотографии продукта
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    products = models.ManyToManyField('Product')
    order_date = models.DateTimeField(default=timezone.now)

    @property
    def total_amount(self):
        return sum(product.price for product in self.products.all())

    def __str__(self):
        return f"Order #{self.id} by {self.client.name}"



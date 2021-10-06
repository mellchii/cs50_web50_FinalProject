
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Product(models.Model):
    CATEGORY = [
        ('FR', 'Fruits'),
        ('VG', 'Vegetables'),
        ('MT', 'Meat'),
        ('GR', 'Grains'),
        ('TU', 'Tubers'),
        ('DY', 'Dairy'),
    ]
    name = models.CharField(max_length=30)
    uom = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=6, decimal_places=2,null=True, blank=True)
    category = models.CharField(max_length=2, choices=CATEGORY, default='FR',)
    long_description = models.TextField(max_length=200)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='', blank=True, null=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "stock": self.stock,
            "price": self.price,
            "img_url": self.image.url,
            "avg_rating": self.avg_rating
        }

    def __str__(self):
        return self.name

    @property
    def avg_rating(self):
        reviews = self.reviews_set.all().aggregate(Avg('rating'))
        if not self.reviews_set.all():
            return 1
        return reviews.get('rating__avg', 1)


class Order(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    order_number = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.order_number

    def serialize(self):
        return {
            "order_number": self.order_number,
            "item_total": self.item_total,
        }

    @property
    def cart_total(self):
        order_items = self.orderitem_set.all()
        total = 0
        for item in order_items:
            total += item.get_total
        return total

    @property
    def item_total(self):
        order_items = self.orderitem_set.all()
        total = 0
        for item in order_items:
            total += item.quantity
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total


class Checkout(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.order.order_number

class Reviews(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    review = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=1, validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])

    def serialize(self):
        return {
            "product": self.product.name,
            "review": self.review,
            "rating": self.rating,
        }

    def __str__(self):
        return self.product.name

class Wishlist(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

class Supply(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    supply_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
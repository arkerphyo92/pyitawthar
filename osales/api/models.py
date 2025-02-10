import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class User(AbstractUser):
    pass

    
class ProductCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

class Product(models.Model):
    class StatusChoices(models.TextChoices):
        AVAILABLE = "Available",
        UNAVAILABLE = "Unavailable",

    name = models.CharField(max_length=200)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.AVAILABLE)

    @property
    def in_stock(self):
        return self.stock > 0
    
    @property
    def discounted_price(self):
        active_discount = self.discounts.filter(start_date__lte=datetime.datetime.now(), end_date__gte=datetime.datetime.now()).first()
        if active_discount:
            return self.price * ( 1 - active_discount.discount_percentage / 100)
        
    def __str__(self):
        return self.name


class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="discounts")
    discount_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    @property
    def is_active(self):
        return self.start_date <= datetime.datetime.now() <= self.end_date

    def __str__(self):
        return f"{self.discount_percentage}% discount on {self.product.name} from {self.start_date} to {self.end_date}"

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending",
        COMPLETED = "Completed",
        CANCELLED = "Cancelled"
    
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name} - Order {self.order.order_id}"







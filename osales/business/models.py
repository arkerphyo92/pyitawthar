import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import uuid
# Create your models here.

class PayTypeChoices(models.TextChoices):
        KG = "kg"
        GRAM = "g"
        PCS = "pcs"
        SET = "Sets"
        DOZEN = "Dozen"

class WeightTypeChoices(models.TextChoices):
        KG = "kg"
        GRAM = "g"

class ProductStatusChoices(models.TextChoices):
        AVAILABLE = "Available"
        UNAVAILABLE = "Unavailable"

class OrderStatusChoices(models.TextChoices):
        CONFIRMED = "Confirmed"
        APPROVED = "Approved"
        COMPLETED = "Completed"
        CANCELLED = "Cancelled"

class User(AbstractUser):
    pass

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True
    
class ProductCategory(TimestampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories")

    def __str__(self):
        return f"{self.parent.name} -> {self.name}" if self.parent else self.name
    
    class Meta:
        verbose_name_plural = "Product Categories"

class CategoryImage(TimestampedModel):
    product_category = models.OneToOneField(ProductCategory, on_delete=models.CASCADE, related_name='categoryimages')
    image = models.ImageField(upload_to="category_images/")
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image of {self.product_category.name}"
    
    class Meta:
        verbose_name_plural = "Product Images"

class ExchangeRate(TimestampedModel):
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.exchange_rate}"
    
    class Meta:
        verbose_name_plural = "Exchange Rates"    


class Product(TimestampedModel):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, related_name="products")
    description = models.TextField()
    arrival_date = models.DateField(auto_now_add=True)
    stock = models.PositiveIntegerField()
    stock_type = models.CharField(max_length=20, choices=PayTypeChoices.choices, default=PayTypeChoices.PCS)
    exchange_rate = models.ForeignKey(ExchangeRate, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=ProductStatusChoices.choices, default=ProductStatusChoices.AVAILABLE, )
    sold = models.PositiveIntegerField(default=0)

    @property
    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Products"


class Price(TimestampedModel):    
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="prices")
    
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    retail_price_per = models.DecimalField(max_digits=10, decimal_places=2)
    retail_pay_type = models.CharField(max_length=20, choices=PayTypeChoices.choices, default=PayTypeChoices.PCS)

    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    wholesale_price_per = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    wholesale_pay_type = models.CharField(max_length=20, choices=PayTypeChoices.choices, default=PayTypeChoices.PCS)
    @property
    def retail_price_with_discount(self):
        active_discount = self.product.discounts
        if active_discount:
            final_retail_discounted_price = self.retail_price * ( 1 - active_discount.retail_discount_percentage / 100)
            return round(final_retail_discounted_price, 2)
        
    
    @property
    def wholesale_price_with_discount(self):
        active_discount = self.product.discounts
        if active_discount:
            final_wholesale_discounted_price = self.wholesale_price * ( 1 - active_discount.wholesale_discount_percentage / 100)
            return round(final_wholesale_discounted_price,2)
    
    def __str__(self):
        return f"{self.retail_price}"
    
    class Meta:
        verbose_name_plural = "Prices"

class Discount(TimestampedModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="discounts")
    retail_discount_percentage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    wholesale_discount_percentage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    @property
    def is_active(self):
        return self.start_date <= datetime.datetime.now() <= self.end_date

    def __str__(self):
        return f"{self.retail_discount_percentage}% discount on {self.product.name}"

    class Meta:
        verbose_name_plural = "Discounts"


class ProductReview(TimestampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review = models.TextField()

    def __str__(self):
        return f"{self.user.username} - Review of {self.product.name}"
    
    class Meta:
        verbose_name_plural = "Product Reviews"
    

class ProductImage(TimestampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="product_images/")
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image of {self.product.name}"
    
    class Meta:
        verbose_name_plural = "Product Images"


class Order(TimestampedModel):    
    
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="approved_by_adminteam")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, choices=OrderStatusChoices.choices, default=OrderStatusChoices.CONFIRMED)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"
    
    class Meta:
        verbose_name_plural = "Orders"
    
class OrderItem(TimestampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} - Order {self.order.order_id}"

    class Meta:
        verbose_name_plural = "Order Items"




class UserCart(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    class Meta:
        verbose_name_plural = "User Carts"

class CartItem(TimestampedModel):
    cart = models.ForeignKey(UserCart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    retail_type = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} - Cart {self.cart.id}"
    
    class Meta:
        verbose_name_plural = "Cart Items"
        unique_together = ('cart', 'product')

    @property
    def total_price_for_cart_item(self):
        price = self.product.prices
        if self.retail_type:
            if price.retail_price_with_discount:
                return price.retail_price_with_discount * self.quantity
            return self.product.prices.retail_price * self.quantity
        else:
            if price.wholesale_price_with_discount:
                return price.wholesale_price_with_discount * self.quantity
            return self.product.prices.wholesale_price * self.quantity
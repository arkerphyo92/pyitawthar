from django.contrib import admin
from .models import User, Order, OrderItem, Product, ProductCategory, Discount

# Register your models here.
admin.site.register(User)
admin.site.register(ProductCategory)
admin.site.register(Discount)

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
        ]

admin.site.register(Order, OrderAdmin)

class ProductDiscountInline(admin.TabularInline):
    model = Discount

class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductDiscountInline
        ]
    list_display = ['name', 'category', 'price', 'stock', 'status', 'discounted_price']
    readonly_fields = ['discounted_price']
    
admin.site.register(Product, ProductAdmin)
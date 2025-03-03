from django.contrib import admin
from .models import CartItem, CategoryImage, ProductImage, User, Order, OrderItem, Product, ProductCategory, Discount, ExchangeRate, Price, UserCart
from django.conf import settings
from django.utils.safestring import mark_safe
from django.templatetags.static import static



# Register your models here.
admin.site.register(User)

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
        ]
    list_display = ['order_id', 'user', 'status', 'total_price', 'approved_by']
    list_editable = ['status']
    list_per_page = settings.LIST_PER_PAGE
    readonly_fields = ['user', 'total_price', 'approved_by']
    
    def total_price(self, obj):
        all_items = obj.items.all()
        return sum(item.sub_total for item in all_items)
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        
        if "status" in form.changed_data:
            obj.approved_by = request.user

        super().save_model(request, obj, form, change)
    
admin.site.register(Order, OrderAdmin)

class ProductDiscountInline(admin.TabularInline):
    model = Discount

class ProductImageInline(admin.TabularInline):
    model = ProductImage

class PriceInline(admin.TabularInline):
    model = Price

class ProductAdmin(admin.ModelAdmin):
    def in_stock(self, obj):        
        if obj.stock > 5:
            return mark_safe(
                f'<img src="{static("enough_stock.svg")}" title="Stock is greater than 5"  alt="enough-stock"/>'
            )
        else:
            # Corrected the usage of format to properly include the static path
            return mark_safe(
                f'<img src="{static("lower_stock.svg")}" title="Stock is lower than 5" alt="lower-stock"/>'
            )
    
    inlines = [
        PriceInline,
        ProductDiscountInline,
        ProductImageInline,
        ]
    
    @admin.display(description=("Retail"), ordering="prices.retail_price")
    def retail_price_detail_view(self, obj):
        return obj.prices.retail_price
    
    @admin.display(description=("Wholesale"), ordering="prices.wholesale_price")
    def wholesale_price_detail_view(self, obj):
        return obj.prices.wholesale_price

    
    @admin.display(description=("Discounted Retail"), ordering="prices.retail_price_with_discount")
    def prices_retail_discount_view(self, obj):
        return obj.prices.retail_price_with_discount
    
    @admin.display(description=("Discounted Wholesale"), ordering="prices.wholesale_price_with_discount")
    def prices_wholesale_discount_view(self, obj):
        return obj.prices.wholesale_price_with_discount
    
    list_display = ['name', 'category', 'stock', 'retail_price_detail_view',  'wholesale_price_detail_view', 'prices_retail_discount_view', 'prices_wholesale_discount_view','status', 'in_stock']
    list_editable = ['stock', 'status']
    list_per_page = settings.LIST_PER_PAGE
    list_filter = ['category','status']
    
    # readonly_fields = ['retail_price_with_discount']
    # autocomplete_fields = ['category']

    
admin.site.register(Product, ProductAdmin)

class CategoryImageInline(admin.TabularInline):
    model = CategoryImage

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        CategoryImageInline,
        ]
    list_per_page = settings.LIST_PER_PAGE

admin.site.register(ProductCategory, CategoryAdmin)

class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ['currency', 'exchange_rate', 'created_at']
    list_editable = ['exchange_rate']
    list_per_page = settings.LIST_PER_PAGE

admin.site.register(ExchangeRate, ExchangeRateAdmin)

class DiscountAdmin(admin.ModelAdmin):
    # list_display = ['product', 'discount_percentage','start_date', 'end_date']
    # list_editable = ['discount_percentage']
    list_per_page = settings.LIST_PER_PAGE

admin.site.register(Discount, DiscountAdmin)

class UserCartAdmin(admin.ModelAdmin):
    list_per_page = settings.LIST_PER_PAGE

admin.site.register(UserCart, UserCartAdmin)

class CartItemAdmin(admin.ModelAdmin):
    list_per_page = settings.LIST_PER_PAGE

admin.site.register(CartItem, CartItemAdmin)


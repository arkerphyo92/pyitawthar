from rest_framework import serializers
from api.models import Discount, Product, User, Order, OrderItem

class DiscountSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ("discount_percentage", "start_date", "end_date")


class ProductSerializer(serializers.ModelSerializer):
    discounts = DiscountSerilizer(many=True, read_only=True)
    discounted_price = serializers.SerializerMethodField

    class Meta:
        model = Product
        fields = ("name", "description", "price", "stock", "discounts", "discounted_price")

    def get_discounted_price(self, obj):
        return obj.discounted_price
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive number")
        return value
    
   

class OrderItemSerializer(serializers.ModelSerializer):
    # product_name = serializers.SerializerMethodField()
    product_name = serializers.CharField(source="product.name")
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2, source="product.price")

    def get_product_name(self, obj):
        return obj.product.name
    def get_product_price(self, obj):
        return obj.product.price

    class Meta:
        model = OrderItem
        fields = ("order", "product","product_name", "product_price", "quantity", "sub_total")

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    def get_total_price(self, obj):
        all_items = obj.items.all()
        return sum(item.sub_total for item in all_items)

    class Meta:
        model = Order
        fields = ("order_id", "user", "status", "items", "total_price")


class ProductInfoSerilizer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()



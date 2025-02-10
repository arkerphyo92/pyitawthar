from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Max
from .models import Product, Order, OrderItem, User
from django.http import JsonResponse
from .serializers import ProductInfoSerilizer, ProductSerializer, OrderSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions



# Create your views here.

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer


# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related(
        "items__product"
    ).all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(user=user)


@api_view(['GET'])
def products_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerilizer({
        "products": products,
        "count" : len(products),
        "max_price": products.aggregate(max_price=Max('price'))['max_price']
        })
    return Response(serializer.data)
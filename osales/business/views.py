from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Max
from .models import Product, Order, OrderItem, User
from django.http import JsonResponse


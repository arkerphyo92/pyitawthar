from django.shortcuts import get_object_or_404
from ninja import Query, Router, File
from ninja.files import UploadedFile
from ninja_jwt.authentication import JWTAuth
from ninja.pagination import paginate, PageNumberPagination
from ninja.errors import HttpError

from django.db import transaction, IntegrityError

from business.schema.products import ProductFilterSchema, ProductListSchema, SingleProductSchemaOut, SingleProductSchemaIn
from business.models import Discount, ExchangeRate, Price, Product, ProductCategory, ProductImage, User

from typing import List

productsapi = Router(tags=["Products"])


@productsapi.get("/list", response=list[ProductListSchema])
@paginate(PageNumberPagination, page_size=10)
def product_list(request, filters: ProductFilterSchema = Query(...)):
    products = Product.objects.all()
    products = filters.filter(products)
    return products

@productsapi.post("/product", response=SingleProductSchemaOut, auth=JWTAuth())
def create_product(request, payload: SingleProductSchemaIn, file: List[UploadedFile] = File(...)):
    try:
        with transaction.atomic():
            product_obj = payload.model_dump(exclude_unset=True, exclude_none=True, exclude=['prices', 'discounts'])
            prices_obj = payload.prices.model_dump(exclude_unset=True, exclude_none=True)
            discounts_obj = payload.discounts.model_dump(exclude_unset=True, exclude_none=True)
            
            if payload.category:
                product_category = get_object_or_404(ProductCategory, id=payload.category)
                product_obj['category'] = product_category

            if payload.exchange_rate:
                product_exchange_rate = get_object_or_404(ExchangeRate, id=payload.exchange_rate)
                product_obj['exchange_rate'] = product_exchange_rate

            user = get_object_or_404(User, id=request.auth.id)
            product_obj['user'] = user

            product = Product.objects.create(**product_obj)

            if prices_obj:
                Price.objects.create(**prices_obj, product=product, user=request.auth)

            if discounts_obj:
                Discount.objects.create(**discounts_obj, product=product)

            if file:
                for img in file:
                    ProductImage.objects.create(product=product, image=img, user=user)

            return product
    except IntegrityError as e:
        raise HttpError(400, f"Database integrity error, transaction rolled back. {e}")

@productsapi.get("/{product_id}", response=SingleProductSchemaOut)
def get_product(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    return product
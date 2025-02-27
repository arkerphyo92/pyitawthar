from ninja import Router, File
from ninja.files import UploadedFile
from ninja_jwt.authentication import JWTAuth
from ninja.pagination import paginate, PageNumberPagination

from business.schema.products import ProductListSchema, SingleProductSchemaOut, SingleProductSchemaIn
from business.models import Product

from typing import List

productsapi = Router(tags=["Products"])


@productsapi.post("/list", response=list[ProductListSchema], auth=JWTAuth())
@paginate(PageNumberPagination, page_size=10)
def product_list(request):
    products = Product.objects.all()
    return products

@productsapi.post("/product")
def create_product(request, payload: SingleProductSchemaIn, file: List[UploadedFile] = File(...)):
    raw_obj = payload.model_dump(exclude_unset=True, exclude_none=True, exclude=['category', 'prices', 'discounts'])
    product = Product.objects.create(**payload.dict())
    return product

@productsapi.get("/{product_id}", response=SingleProductSchemaOut)
def get_product(request, product_id: int):
    product = Product.objects.get(id=product_id)
    return product
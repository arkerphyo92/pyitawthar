from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate, PageNumberPagination
from business.models import ProductCategory
from ninja_jwt.authentication import JWTAuth
from business.schema.categories import CategorySchemaOut, CategoryFilterSchema

categoriesapi = Router(tags=["Categories"])

@categoriesapi.get("/list", response=list[CategorySchemaOut])
@paginate(PageNumberPagination, page_size=10)
def product_category_list(request, filters: CategoryFilterSchema = Query(...)):
    product_categories = ProductCategory.objects.all().select_related('parent')
    return filters.filter(product_categories)


@categoriesapi.get("/{category_name}", response=CategorySchemaOut)
def get_category(request, category_name: str):
    category = get_object_or_404(ProductCategory, name=category_name)
    return category
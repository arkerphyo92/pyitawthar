from ninja import Router
from ninja.pagination import paginate, PageNumberPagination
from business.models import ProductCategory
from ninja_jwt.authentication import JWTAuth
from business.schema.categories import CategorySchemaOut

categoriesapi = Router(tags=["Categories"])

@categoriesapi.post("/list", response=list[CategorySchemaOut])
@paginate(PageNumberPagination, page_size=10)
def product_category_list(request):
    product_categories = ProductCategory.objects.all()
    return product_categories
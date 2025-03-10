import datetime
from ninja import FilterSchema, Schema
from pydantic import Field
from business.models import ProductCategory, ProductImage

class CategorySchema(Schema):
    name: str

class ProductImageSchema(Schema):
    image: str


class DiscountsSchemaOut(Schema):
    retail_discount_percentage: float | None
    wholesale_discount_percentage: float | None
    start_date: datetime.datetime | None
    end_date: datetime.datetime | None


class DiscountsSchemaIn(Schema):
    retail_discount_percentage: float | None
    wholesale_discount_percentage: float | None
    start_date: datetime.datetime | None
    end_date: datetime.datetime | None


class PriceSchemaOut(Schema):
    retail_price: float
    wholesale_price: float | None
    retail_price_with_discount: float | None = None
    wholesale_price_with_discount: float | None = None
    retail_pay_type: str
    wholesale_pay_type: str | None


class ProductListSchema(Schema):
    id: int
    name: str
    description: str
    category: str
    status: str
    in_stock: bool | None
    prices: PriceSchemaOut | None
    images: list[ProductImageSchema]
    discounts: DiscountsSchemaOut | None = None

    @staticmethod
    def resolve_category(obj):
        if obj.category:
            parent = obj.category.parent.name if obj.category.parent else "No Parent"
            return f"{obj.category.name}" if parent else obj.category.name
        return "No Category"

    
class SingleProductSchemaOut(Schema):
    id: int
    name: str
    description: str
    category: str
    stock: float | None
    stock_type: str
    status: str
    in_stock: bool
    sold: int
    prices: PriceSchemaOut | None = None
    discounts: DiscountsSchemaOut | None = None
    images: list[ProductImageSchema]
    user: str

    @staticmethod
    def resolve_user(obj):
        return obj.user.username

    @staticmethod
    def resolve_category(obj):
        return obj.category.name if obj.category else "No Category"


class PriceSchemaIn(Schema):
    retail_price: float = Field(..., example="Decimal Number")
    retail_price_per: float = Field(..., example="Decimal Number")
    retail_pay_type: str = Field(..., example="KG or GRAM or PCS or SET or DOZEN")
    wholesale_price: float | None = Field(..., example="Decimal Number")
    wholesale_price_per: float | None = Field(..., example="Decimal Number")
    wholesale_pay_type: str | None = Field(..., example="KG or GRAM or PCS or SET or DOZEN")


class SingleProductSchemaIn(Schema):
    name: str
    description: str
    category: int = Field(..., example="ID")
    arrival_date: datetime.datetime
    stock: float | None = Field(..., example="Positive Integer")
    stock_type: str = Field(..., example="KG or GRAM or PCS or SET or DOZEN")
    weight: float | None = Field(..., example="Positive Integer")
    weight_type: str = Field(..., example="KG or GRAM")
    exchange_rate: int | None = Field(..., example="Exchange Rate ID")
    status: str = Field(..., example="AVAILABLE or UNAVAILABLE")
    prices: PriceSchemaIn | None
    discounts: DiscountsSchemaIn | None


class ProductFilterSchema(FilterSchema):
    search: str | None = Field(None, q=['name__icontains', 'category__name__icontains'])
    category_name: str | None = Field(None, q="category__name__iexact",title="Category Filter",
        description="Filter products by category name (case-insensitive)")

    def filter(self, queryset):
        if self.category_name:
            parent_category = ProductCategory.objects.filter(name__iexact=self.category_name).first()
            if parent_category:
                sub_categories_ids = parent_category.subcategories.values_list("id", flat=True)
                queryset = queryset.filter(category__in=[parent_category.id]+list(sub_categories_ids))
            else:
                queryset = queryset.filter(category=None)

        if self.search:
            queryset = queryset.filter(name__icontains=self.search) | queryset.filter(category__name__icontains=self.search)
            
        return queryset




class ReviewShemaOut(Schema):
    id: int
    product: int
    user: int
    review: str
    rating: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

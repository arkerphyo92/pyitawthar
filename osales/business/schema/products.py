import datetime
from ninja import Schema

class CategorySchema(Schema):
    name: str

class ProductImageSchema(Schema):
    image: str

class DiscountsSchema(Schema):
    retial_discount_percentage: float | None
    wholesale_discount_percentage: float | None
    start_date: str | None
    end_date: str | None

class PriceSchema(Schema):
    retail_price: float | None
    wholesale_price: float | None
    retail_price_with_discount: float | None = None
    wholesale_price_with_discount: float | None = None

class ProductListSchema(Schema):
    id: int
    name: str
    category: str
    stock: float | None
    status: str
    in_stock: bool | None
    prices: PriceSchema | None
    images: list[ProductImageSchema]

    @staticmethod
    def resolve_category(obj):
        return obj.category.name if obj.category else "No Category"


class SingleProductSchemaOut(Schema):
    id: int
    name: str
    description: str
    category: str
    stock: float | None
    stock_type: str
    weight: float | None
    weight_type: str
    status: str
    in_stock: bool | None
    prices: PriceSchema | None
    discounts: list[DiscountsSchema] | None
    images: list[ProductImageSchema]


class SingleProductSchemaIn(Schema):
    name: str
    description: str
    category: str
    arrival_date: datetime.datetime
    stock: float | None
    stock_type: str
    weight: float | None
    weight_type: str
    exchange_rate: str | None
    status: str
    prices: PriceSchema | None
    discounts: DiscountsSchema | None
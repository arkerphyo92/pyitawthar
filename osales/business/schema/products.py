import datetime
from ninja import FilterSchema, Schema
from pydantic import Field


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


class ProductListSchema(Schema):
    id: int
    name: str
    category: str
    stock: float | None
    status: str
    in_stock: bool | None
    prices: PriceSchemaOut | None
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
    in_stock: bool
    sold: int
    prices: PriceSchemaOut | None = None
    discounts: DiscountsSchemaOut | None = None
    images: list[ProductImageSchema]

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
    category: int | None = None


class ReviewShemaOut(Schema):
    id: int
    product: int
    user: int
    review: str
    rating: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

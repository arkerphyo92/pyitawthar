from ninja import Schema
from pydantic import Field
from business.models import ProductCategory

class CategorySchemaOut(Schema):
    id: int
    name: str
    description: str
    parent: int | None
    cat_image: str | None = None
    products_count: int | None = 0 

    @staticmethod
    def resolve_cat_image(obj):
        return obj.categoryimages.image if obj.categoryimages.image else "No Image"
    
    @staticmethod
    def resolve_parent(obj):
        return obj.parent.id if obj.parent else 0

    @staticmethod
    def resolve_products_count(obj):
        all_data = obj.products if obj.products else None
        total_products = all_data.count()

        subcategories = obj.subcategories.all() if obj.subcategories else []
        for subcategory in subcategories:
            total_products += subcategory.products.count()
        
        return total_products


class CategoryFilterSchema(Schema):
    parent_cat_name: str | None = Field(None, q="parent__name__iexact",title="Sub Categories Filter",
        description="Select Sub Categories by parent category name (case-insensitive)")

    def filter(self, queryset):
        if self.parent_cat_name:
            parent_category = ProductCategory.objects.filter(name__iexact=self.parent_cat_name).first()
            if parent_category:
                return queryset.filter(parent=parent_category)
            else:
                return queryset(parent=None)
        return queryset
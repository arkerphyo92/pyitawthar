from ninja import Schema

class CategorySchemaOut(Schema):
    id: int
    name: str
    description: str
    parent: int | None
    cat_image: str | None = None

    @staticmethod
    def resolve_cat_image(obj):
        return obj.categoryimages.image if obj.categoryimages.image else "No Image"
    
    @staticmethod
    def resolve_parent(obj):
        return obj.parent.id if obj.parent else 0
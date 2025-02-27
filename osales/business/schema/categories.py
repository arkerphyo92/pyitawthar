from ninja import Schema

class CategorySchemaOut(Schema):
    id: int
    name: str
    description: str
    parent: int | None

    @staticmethod
    def resolve_parent(obj):
        return obj.parent.id if obj.parent else 0
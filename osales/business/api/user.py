from ninja import Router
from ninja_jwt.authentication import JWTAuth

from business.schema.user_schema import UserSchema

userandauthapi = Router(tags=["User and Authentication"])


@userandauthapi.post("/me", response=UserSchema, auth=JWTAuth())
def me(request):
    return UserSchema.model_validate(request.user)
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

from business.api.user import userandauthapi
from business.api.products import productsapi
from business.api.categories import categoriesapi

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

api.add_router('', userandauthapi)
api.add_router('/products/', productsapi)
api.add_router('/categories/', categoriesapi)
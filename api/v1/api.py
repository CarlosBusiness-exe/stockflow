from fastapi import APIRouter

from api.v1.endpoints import product
from api.v1.endpoints import category
from api.v1.endpoints import supplier
from api.v1.endpoints import user

api_router = APIRouter()
api_router.include_router(product.router, prefix="/products", tags=["products"])
api_router.include_router(category.router, prefix="/categories", tags=["categories"])
api_router.include_router(supplier.router, prefix="/suppliers", tags=["suppliers"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
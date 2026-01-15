from typing import Optional
from sqlmodel import SQLModel

from schemas.product_schema import ProductSchemaResponse

class CategorySchemaBase(SQLModel):
    name: str

class CategorySchemaResponse(CategorySchemaBase):
    id: int

class CategorySchemaProducts(CategorySchemaResponse):
    products: List[ProductSchemaResponse] = []
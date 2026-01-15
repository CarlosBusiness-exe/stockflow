from typing import Optional
from sqlmodel import SQLModel

class ProductSchemaBase(SQLModel):
    name: str
    price: float
    qtd: int
    category_id: int
    supplier_id: int

class ProductSchemaCreate(ProductSchemaBase):
    pass

class ProductSchemaResponse(ProductSchemaBase):
    id: int
from typing import Optional

from sqlmodel import SQLModel, Field

class ProductModel(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    qtd: int
    
    category_id: Optional[int] = Field(default=None, foreign_key="categories.id")
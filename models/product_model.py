from typing import Optional

from sqlmodel import SQLModel, Field

class ProductModel(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: str
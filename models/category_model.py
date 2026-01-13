from typing import Optional, List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.product_model import ProductModel

class CategoryModel(SQLModel, table=True):
    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)

    products: List["ProductModel"] = Relationship(back_populates="category")
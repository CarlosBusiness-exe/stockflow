from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.category_model import CategoryModel
    from models.supplier_model import SupplierModel

class ProductModel(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    qtd: int
    
    category_id: int = Field(default=None, foreign_key="categories.id")
    supplier_id: int = Field(default=None, foreign_key="suppliers.id")

    category: Optional["CategoryModel"] = Relationship(back_populates="products")
    supplier: Optional["SupplierModel"] = Relationship(back_populates="products")
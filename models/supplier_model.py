from typing import Optional, List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.product_model import ProductModel

class SupplierModel(SQLModel, table=True):
    __tablename__ = "suppliers"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    cnpj: str = Field(unique=True)
    address: str

    products: List["ProductModel"] = Relationship(back_populates="suppliers")
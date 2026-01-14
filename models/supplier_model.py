from typing import Optional, List, TYPE_CHECKING

from sqlmodel import Field, Relationship

from schemas.supplier_schema import SupplierSchemaBase

if TYPE_CHECKING:
    from models.product_model import ProductModel

class SupplierModel(SupplierSchemaBase, table=True):
    __tablename__ = "suppliers"

    id: Optional[int] = Field(default=None, primary_key=True)
    cnpj: str = Field(unique=True)

    products: List["ProductModel"] = Relationship(back_populates="supplier")
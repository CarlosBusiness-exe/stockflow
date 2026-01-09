from typing import Optional

from sqlmodel import SQLModel, Field

class SupplierModel(SQLModel, table=True):
    __tablename__ = "suppliers"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    cnpj: str = Field(unique=True)
    address: str
from typing import Optional
from sqlmodel import SQLModel

class SupplierSchemaBase(SQLModel):
    name: str
    cnpj: str
    address: str

class SupplierSchemaResponse(SupplierSchemaBase):
    id: int
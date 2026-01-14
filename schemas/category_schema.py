from typing import Optional
from sqlmodel import SQLModel

class CategorySchemaBase(SQLModel):
    name: str

class CategorySchemaResponse(CategorySchemaBase):
    id: int
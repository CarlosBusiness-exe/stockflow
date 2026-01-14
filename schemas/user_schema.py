from typing import Optional
from sqlmodel import SQLModel

class UserSchemaBase(SQLModel):
    name: str
    email: str
    is_admin: bool

class UserSchemaCreate(UserSchemaBase):
    password: str

class UserSchemaResponse(UserSchemaBase):
    id: int
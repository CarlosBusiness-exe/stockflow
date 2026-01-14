from typing import Optional

from sqlmodel import SQLModel, Field

from schemas.user_schema import UserSchemaBase

class UserModel(UserSchemaBase, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    password: str
from typing import Optional

from sqlmodel import SQLModel, Field

class UserModel(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    email: str = Field(unique=True, index=True)
    password: str
    is_admin: bool = Field(default=False)
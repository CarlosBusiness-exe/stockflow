from pytz import timezone

from typing import Optional, List
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt

from models.user_model import UserModel
from core.configs import settings
from core.security import verify_password

from pydantic import EmailStr

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/users/login" 
)

async def authenticate(email: EmailStr, password: str, db: AsyncSession):
    async with db as session:
        query = select(UserModel).where(UserModel.email == email)
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        
        return user

def _create_token(type_token: str, time_token: timedelta, sub: str) -> str: 
    payload = {}

    sp = timezone("America/Sao_Paulo")
    expires = datetime.now(tz=sp) + time_token

    payload["type"] = type_token

    payload["exp"] = expires

    payload["iat"] = datetime.now(tz=sp)

    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def create_token_access(sub: str) -> str:
    return _create_token(
        type_token="access_token",
        time_token=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )
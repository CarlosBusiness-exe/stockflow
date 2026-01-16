from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user_model import UserModel
from schemas.user_schema import UserSchemaBase, UserSchemaCreate, UserSchemaResponse
from core.deps import get_session, get_current_user
from core.security import generate_hash
from core.auth import authenticate, create_token_access

router = APIRouter()

#GET LOGGED
@router.get("/logged", response_model=UserSchemaBase)
def get_logged(logged_user: UserModel = Depends(get_current_user)):
    return logged_user


#POST/SIGNUP
@router.post("/signup", response_model=UserSchemaBase, status_code=status.HTTP_201_CREATED)
async def post_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
    new_user = UserModel.model_validate(user)

    new_user.password = generate_hash(user.password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


#GET USERS
@router.get("/", response_model=List[UserSchemaResponse])
async def get_users(db: AsyncSession = Depends(get_session)):
    query = select(UserModel)
    result = await db.execute(query)
    users: List[UserModel] = result.scalars().unique().all()

    return users


#GET USER
@router.get("/{user_id}", response_model=UserSchemaResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    query = select(UserModel).where(UserModel.id == user_id)
    result = await db.execute(query)
    user = result.scalars().unique().one_or_none()

    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

#PUT USER
@router.put("/{user_id}", response_model=UserSchemaResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_user(user_id: int, user: UserSchemaCreate, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    query = select(UserModel).where(UserModel.id == user_id)
    result = await db.execute(query)
    user_up: UserSchemaResponse = result.scalars().unique().one_or_none()

    if user_up:
        user_data = user.model_dump(exclude_unset=True)

        if "password" in user_data:
            user_data["password"] = generate_hash(user_data["password"])

        db.add(user_up)
        await db.commit()
        await db.refresh(user_up)

        return user_up
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")


#DELETE USER
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    query = select(UserModel).where(UserModel.id == user_id)
    result = await db.execute(query)
    user_del: UserModel = result.scalars().unique().one_or_none()

    if user_del:
        await db.delete(user_del)
        await db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

#POST/LOGIN
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await authenticate(email=form_data.username, password=form_data.password, db=db)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The data is incorrect")

    return {"access_token": create_token_access(user.id), "token_type": "bearer"}
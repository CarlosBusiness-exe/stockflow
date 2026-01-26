from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.category_model import CategoryModel
from models.user_model import UserModel
from schemas.category_schema import CategorySchemaBase, CategorySchemaResponse, CategorySchemaProducts
from core.deps import get_session, get_current_user
from services.category_service import CategoryService

router = APIRouter()


#POST
@router.post("/", response_model=CategorySchemaResponse, status_code=status.HTTP_201_CREATED)
async def post_category(category: CategorySchemaBase, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    return await CategoryService.create_category(category, db)


#GET CATEGORIES
@router.get("/", response_model=List[CategorySchemaResponse], status_code=status.HTTP_200_OK)
async def get_categories(db: AsyncSession = Depends(get_session)):
    query = select(CategoryModel).order_by(CategoryModel.id)
    result = await db.execute(query)
    categories :List[CategoryModel] = result.scalars().all()

    return categories


#GET CATEGORY
@router.get("/{category_id}", response_model=CategorySchemaProducts, status_code=status.HTTP_200_OK)
async def get_category(category_id: int, db: AsyncSession = Depends(get_session)):
    return await CategoryService.get_category_by_id(category_id, db)
    

#PUT CATEGORY
@router.put("/{category_id}", response_model=CategorySchemaResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_category(category_id: int, category: CategorySchemaBase, db: AsyncSession = Depends(get_session), user_logged: UserModel = Depends(get_current_user)):
   return await CategoryService.update_category(category_id, category, db)
    

#DELETE CATEGORY
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_session), user_logged: UserModel = Depends(get_current_user)):
    await CategoryService.delete_category(category_id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
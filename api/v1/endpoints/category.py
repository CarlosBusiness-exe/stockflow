from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.category_model import CategoryModel
from core.deps import get_session

router = APIRouter()


#POST
@router.post("/", response_model=CategoryModel, status_code=status.HTTP_201_CREATED)
async def post_category(category: CategoryModel, db: AsyncSession = Depends(get_session)):
    new_category = CategoryModel(name = category.name)

    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)

    return new_category


#GET CATEGORIES
@router.get("/", response_model=List[CategoryModel], status_code=status.HTTP_200_OK)
async def get_categories(db: AsyncSession = Depends(get_session)):
    query = select(CategoryModel).order_by(CategoryModel.id)
    result = await db.execute(query)
    categories :List[CategoryModel] = result.scalars().all()

    return categories


#GET CATEGORY
@router.get("/{category_id}", response_model=CategoryModel, status_code=status.HTTP_200_OK)
async def get_category(category_id: int, db: AsyncSession = Depends(get_session)):
    query = select(CategoryModel).where(CategoryModel.id == category_id)
    result = await db.execute(query)
    category = result.scalar_one_or_none()

    if category:
        return category
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found!")
    

#PUT CATEGORY
@router.put("/{category_id}", response_model=CategoryModel, status_code=status.HTTP_202_ACCEPTED)
async def put_category(category_id: int, category: CategoryModel, db: AsyncSession = Depends(get_session)):
    query = select(CategoryModel).where(CategoryModel.id == category_id)
    result = await db.execute(query)
    category_up = result.scalar_one_or_none()

    if category_up:
        category_up.name = category.name

        await db.commit()
        await db.refresh(category_up)

        return category_up
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    

#DELETE CATEGORY
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_session)):
    query = select(CategoryModel).where(CategoryModel.id == category_id)
    result = await db.execute(query)
    category_del = result.scalar_one_or_none()

    if category_del:
        await db.delete(category_del)
        await db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from models.product_model import ProductModel
from models.user_model import UserModel
from sqlalchemy.exc import IntegrityError
from schemas.product_schema import ProductSchemaCreate, ProductSchemaResponse
from core.deps import get_session, get_current_user
from services.product_service import ProductService

router = APIRouter()


#POST
@router.post("/", response_model=ProductSchemaResponse, status_code=status.HTTP_201_CREATED)
async def post_product(product: ProductSchemaCreate, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    return await ProductService.create_product(product, db)


#GET PRODUCTS
@router.get("/", response_model=List[ProductSchemaResponse], status_code=status.HTTP_200_OK)
async def get_products(db: AsyncSession = Depends(get_session)):
    return await ProductService.get_all_products(db)


#GET PRODUCT
@router.get("/{product_id}", response_model=ProductSchemaResponse, status_code=status.HTTP_200_OK)
async def get_product(product_id: int, db: AsyncSession = Depends(get_session)):
    return await ProductService.get_product_by_id(product_id, db)
        

#PUT PRODUCT
@router.put("/{product_id}", response_model=ProductSchemaResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_product(product_id: int, product: ProductSchemaCreate, db: AsyncSession = Depends(get_session), user_logged: UserModel = Depends(get_current_user)):
    return await ProductService.update_product(product_id, product, db)


#DELETE PRODUCT
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    await ProductService.delete_product(product_id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
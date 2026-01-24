from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.product_model import ProductModel
from models.user_model import UserModel
from models.category_model import CategoryModel
from models.supplier_model import SupplierModel
from sqlalchemy.exc import IntegrityError
from schemas.product_schema import ProductSchemaCreate, ProductSchemaResponse
from core.deps import get_session, get_current_user
from services import product_service

router = APIRouter()


#POST
@router.post("/", response_model=ProductSchemaResponse, status_code=status.HTTP_201_CREATED)
async def post_product(product: ProductSchemaCreate, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):

    query_cat = select(CategoryModel).where(CategoryModel.id == product.category_id)
    result_cat = await db.execute(query_cat)
    if not result_cat.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id {product.category_id} not found")

    query_sup = select(SupplierModel).where(SupplierModel.id == product.supplier_id)
    result_sup = await db.execute(query_sup)
    if not result_sup.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Supplier with id {product.supplier_id} not found")
    
    new_product = ProductModel.model_validate(product)

    try:
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
        return new_product
    except IntegrityError:
        # Caso ocorra um erro de concorrência (ex: alguém deletou o fornecedor no milissegundo entre a checagem e o save)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error: verify Category and Supplier IDs")


#GET PRODUCTS
@router.get("/", response_model=List[ProductSchemaResponse], status_code=status.HTTP_200_OK)
async def get_products(db: AsyncSession = Depends(get_session)):
    query = select(ProductModel)
    result = await db.execute(query)
    products :List[ProductModel] = result.scalars().all()

    return products


#GET PRODUCT
@router.get("/{product_id}", response_model=ProductSchemaResponse, status_code=status.HTTP_200_OK)
async def get_product(product_id: int, db: AsyncSession = Depends(get_session)):
    query = select(ProductModel).where(ProductModel.id == product_id)
    result = await db.execute(query)
    product = result.scalar_one_or_none()

    if product:
        return product
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!")
        

#PUT PRODUCT
@router.put("/{product_id}", response_model=ProductSchemaResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_product(product_id: int, product: ProductSchemaCreate, db: AsyncSession = Depends(get_session), user_logged: UserModel = Depends(get_current_user)):
    query = select(ProductModel).where(ProductModel.id == product_id)
    result = await db.execute(query)
    product_up = result.scalar_one_or_none()

    if product_up:
        product_data = product.model_dump(exclude_unset=True)

        query_cat = select(CategoryModel).where(CategoryModel.id == product.category_id)
        result_cat = await db.execute(query_cat)
        if not result_cat.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id {product.category_id} not found")

        query_sup = select(SupplierModel).where(SupplierModel.id == product.supplier_id)
        result_sup = await db.execute(query_sup)
        if not result_sup.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Supplier with id {product.supplier_id} not found")

        product_up.sqlmodel_update(product_data)

        try:
            db.add(product_up)
            await db.commit()
            await db.refresh(product_up)
            return product_up
        except IntegrityError:
            # Caso ocorra um erro de concorrência (ex: alguém deletou o fornecedor no milissegundo entre a checagem e o save)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error: verify Category and Supplier IDs")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        

#DELETE PRODUCT
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    query = select(ProductModel).where(ProductModel.id == product_id)
    result = await db.execute(query)
    product_del = result.scalar_one_or_none()

    if product_del:
        await db.delete(product_del)
        await db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
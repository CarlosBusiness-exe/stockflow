from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.product_model import ProductModel
from core.deps import get_session

router = APIRouter()


#POST
@router.post("/", response_model=ProductModel, status_code=status.HTTP_201_CREATED)
async def post_product(product: ProductModel, db: AsyncSession = Depends(get_session)):
    new_product = ProductModel(name = product.name, price = product.price, qtd = product.qtd, category_id=product.category_id, supplier_id=product.supplier_id)

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    return new_product


#GET PRODUCTS
@router.get("/", response_model=List[ProductModel], status_code=status.HTTP_200_OK)
async def get_products(db: AsyncSession = Depends(get_session)):
    query = select(ProductModel)
    result = await db.execute(query)
    products :List[ProductModel] = result.scalars().all()

    return products


#GET PRODUCT
@router.get("/{product_id}", response_model=ProductModel, status_code=status.HTTP_200_OK)
async def get_product(product_id: int, db: AsyncSession = Depends(get_session)):
    query = select(ProductModel).where(ProductModel.id == product_id)
    result = await db.execute(query)
    product = result.scalar_one_or_none()

    if product:
        return product
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!")
        

#PUT PRODUCT
@router.put("/{product_id}", response_model=ProductModel, status_code=status.HTTP_202_ACCEPTED)
async def put_product(product_id: int, product: ProductModel, db: AsyncSession = Depends(get_session)):
    query = select(ProductModel).where(ProductModel.id == product_id)
    result = await db.execute(query)
    product_up = result.scalar_one_or_none()

    if product_up:
        product_up.name = product.name
        product_up.price = product.price
        product_up.qtd = product.qtd
        product_up.category_id = product.category_id
        product_up.supplier_id = product_up.supplier_id

        await db.commit()
        await db.refresh(product_up)

        return product_up
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        

#DELETE PRODUCT
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_session)):
    query = select(ProductModel).where(ProductModel.id == product_id)
    result = await db.execute(query)
    product_del = result.scalar_one_or_none()

    if product_del:
        await db.delete(product_del)
        await db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
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
@router.post("/", response_model=ProductModel, status_code=status.HTTP_200_OK)
async def post_product(product: ProductModel, db: AsyncSession = Depends(get_session)):
    new_product = ProductModel(name = product.name, price = product.price, qtd = product.qtd)

    db.add(new_product)
    await db.commit()

    return new_product

#GET PRODUCTS
@router.get("/", response_model=List[ProductModel], status_code=status.HTTP_200_OK)
async def get_products(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProductModel)
        result = await session.execute(query)
        products :List[ProductModel] = result.scalars().all()

    return products
from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.supplier_model import SupplierModel
from core.deps import get_session

router = APIRouter()


#POST SUPPLIER
@router.post("/", response_model=SupplierModel, status_code=status.HTTP_201_CREATED)
async def get_supplier(supplier: SupplierModel, db: AsyncSession = Depends(get_session)):
    new_supplier = SupplierModel(name=supplier.name, cnpj=supplier.cnpj, address=supplier.address)

    db.add(new_supplier)
    await db.commit()
    await db.refresh(new_supplier)

    return new_supplier

#GET SUPPLIERS
@router.get("/", response_model=List[SupplierModel], status_code=status.HTTP_200_OK)
async def get_suppliers(db: AsyncSession = Depends(get_session)):
    query = select(SupplierModel).order_by(SupplierModel.id)
    result = await db.execute(query)
    suppliers: List[SupplierModel] = result.scalars().all()

    return suppliers


#GET SUPPLIER
@router.get("/{supplier_id}", response_model=SupplierModel, status_code=status.HTTP_200_OK)
async def get_supplier(supplier_id: int, db: AsyncSession = Depends(get_session)):
    query = select(SupplierModel).where(SupplierModel.id == supplier_id)
    result = await db.execute(query)
    supplier = result.scalar_one_or_none()

    if supplier:
        return supplier
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found!")
    

#PUT SUPPLIER
@router.put("/{supplier_id}", response_model=SupplierModel, status_code=status.HTTP_202_ACCEPTED)
async def put_supplier(supplier_id: int, supplier: SupplierModel, db: AsyncSession = Depends(get_session)):
    query = select(SupplierModel).where(SupplierModel.id==supplier_id)
    result = await db.execute(query)
    supplier_up = result.scalar_one_or_none()

    if supplier_up:
        supplier_up.name = supplier.name
        supplier_up.cnpj = supplier.cnpj
        supplier_up.address = supplier.address

        await db.commit()
        await db.refresh(supplier_up)

        return supplier_up
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
    

#DELETE SUPPLIER
@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier(supplier_id: int, db: AsyncSession = Depends(get_session)):
    query = select(SupplierModel).where(SupplierModel.id == supplier_id)
    result = await db.execute(query)
    supplier_del = result.scalar_one_or_none()

    if supplier_del:
        await db.delete(supplier_del)
        await db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
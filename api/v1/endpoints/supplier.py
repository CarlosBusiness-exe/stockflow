from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.supplier_model import SupplierModel
from models.user_model import UserModel
from schemas.supplier_schema import SupplierSchemaBase, SupplierSchemaResponse
from core.deps import get_session, get_current_user

router = APIRouter()


#POST SUPPLIER
@router.post("/", response_model=SupplierSchemaResponse, status_code=status.HTTP_201_CREATED)
async def post_supplier(supplier: SupplierSchemaBase, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    #new_supplier = SupplierModel(name=supplier.name, cnpj=supplier.cnpj, address=supplier.address)
    new_supplier = SupplierModel.model_validate(supplier)

    db.add(new_supplier)
    await db.commit()
    await db.refresh(new_supplier)

    return new_supplier

#GET SUPPLIERS
@router.get("/", response_model=List[SupplierSchemaResponse], status_code=status.HTTP_200_OK)
async def get_suppliers(db: AsyncSession = Depends(get_session)):
    query = select(SupplierModel).order_by(SupplierModel.id)
    result = await db.execute(query)
    suppliers: List[SupplierModel] = result.scalars().all()

    return suppliers


#GET SUPPLIER
@router.get("/{supplier_id}", response_model=SupplierSchemaResponse, status_code=status.HTTP_200_OK)
async def get_supplier(supplier_id: int, db: AsyncSession = Depends(get_session)):
    query = select(SupplierModel).where(SupplierModel.id == supplier_id)
    result = await db.execute(query)
    supplier = result.scalar_one_or_none()

    if supplier:
        return supplier
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found!")
    

#PUT SUPPLIER
@router.put("/{supplier_id}", response_model=SupplierSchemaResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_supplier(supplier_id: int, supplier: SupplierSchemaBase, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    query = select(SupplierModel).where(SupplierModel.id==supplier_id)
    result = await db.execute(query)
    supplier_up = result.scalar_one_or_none()

    if supplier_up:
        supplier_data = supplier.model_dump(exclude_unset=True)
        supplier_up.sqlmodel_update(supplier_data)

        await db.commit()
        await db.refresh(supplier_up)

        return supplier_up
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
    

#DELETE SUPPLIER
@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier(supplier_id: int, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    query = select(SupplierModel).where(SupplierModel.id == supplier_id)
    result = await db.execute(query)
    supplier_del = result.scalar_one_or_none()

    if supplier_del:
        await db.delete(supplier_del)
        await db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
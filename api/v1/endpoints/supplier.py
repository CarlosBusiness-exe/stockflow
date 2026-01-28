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
from services.supplier_service import SupplierService

router = APIRouter()


#POST SUPPLIER
@router.post("/", response_model=SupplierSchemaResponse, status_code=status.HTTP_201_CREATED)
async def post_supplier(supplier: SupplierSchemaBase, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    return await SupplierService.create_supplier(supplier, db)

#GET SUPPLIERS
@router.get("/", response_model=List[SupplierSchemaResponse], status_code=status.HTTP_200_OK)
async def get_suppliers(db: AsyncSession = Depends(get_session)):
    return await SupplierService.get_all_suppliers(db)

#GET SUPPLIER
@router.get("/{supplier_id}", response_model=SupplierSchemaResponse, status_code=status.HTTP_200_OK)
async def get_supplier(supplier_id: int, db: AsyncSession = Depends(get_session)):
    return await SupplierService.get_supplier_by_id(supplier_id, db)
    

#PUT SUPPLIER
@router.put("/{supplier_id}", response_model=SupplierSchemaResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_supplier(supplier_id: int, supplier: SupplierSchemaBase, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    return await SupplierService.update_supplier(supplier_id, supplier, db)
    

#DELETE SUPPLIER
@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier(supplier_id: int, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    return await SupplierService.delete_supplier(supplier_id, db)
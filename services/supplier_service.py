from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models.supplier_model import SupplierModel
from schemas.supplier_schema import SupplierSchemaBase


class SupplierService:
    @staticmethod
    async def create_supplier(supplier_data: SupplierSchemaBase, db: AsyncSession):
        new_supplier = SupplierModel(**supplier_data.model_dump())
        db.add(new_supplier)
        await db.commit()
        await db.refresh(new_supplier)

        return new_supplier
    
    @staticmethod
    async def get_supplier_by_id(supplier_id: int, db: AsyncSession):
        supplier = await db.get(SupplierModel, supplier_id)

        if not supplier:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found.")
        return supplier
    
    @staticmethod
    async def get_all_suppliers(db: AsyncSession):
        query = select(SupplierModel)
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def update_supplier(supplier_id: int, supplier_data: SupplierModel, db: AsyncSession):
        supplier_up = await SupplierService.get_supplier_by_id(supplier_id, db)

        supplier_dict = supplier_data.model_dump(exclude_unset=True)
        supplier_up.sqlmodel_update(supplier_dict)

        await db.commit()
        await db.refresh(supplier_up)

        return supplier_up
    
    @staticmethod
    async def delete_supplier(supplier_id: int, db: AsyncSession):
        supplier_del = await SupplierService.get_supplier_by_id(supplier_id, db)

        await db.delete(supplier_del)
        await db.commit()
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from models.product_model import ProductModel
from models.category_model import CategoryModel
from models.supplier_model import SupplierModel
from schemas.product_schema import ProductSchemaCreate

class ProductService:
    @staticmethod
    async def create_product(product_data: ProductSchemaCreate, db: AsyncSession):
        category = await db.get(CategoryModel, product_data.category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
        
        supplier = await db.get(SupplierModel, product_data.supplier_id)
        if not supplier:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found.")
        
        new_product = ProductModel(**product_data.model_dump())
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
        return new_product
    
    @staticmethod
    async def get_product_by_id(product_id: int, db: AsyncSession):
        product_up = await db.get(ProductModel, product_id)

        if not product_up:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
        return product_up
    
    @staticmethod
    async def get_all_products(db: AsyncSession):
        query = select(ProductModel)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update_product(product_id: int, product_data: ProductSchemaCreate, db: AsyncSession):
        product_up = await ProductService.get_product_by_id(product_id, db)
        
        category = await db.get(CategoryModel, product_data.category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
        
        supplier = await db.get(SupplierModel, product_data.supplier_id)
        if not supplier:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found.")
        
        product_dict = product_data.model_dump(exclude_unset=True)
        product_up.sqlmodel_update(product_dict)

        db.add(product_up)
        await db.commit()
        await db.refresh(product_up)
        return product_up
    
    @staticmethod
    async def delete_product(product_id: int, db: AsyncSession):
        product_del = await ProductService.get_product_by_id(product_id, db)

        await db.delete(product_del)
        await db.commit()
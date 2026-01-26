from sqlmodel.ext.asyncio import AsyncSession
from models.category_model import CategoryModel
from schemas.category_schema import CategorySchemaBase
from fastapi import HTTPException, status

class CategoryService:
    @staticmethod
    async def create_category(category_data: CategorySchemaBase, db: AsyncSession):
        new_category = CategoryModel(**category_data.model_dump())
        db.add(new_category)
        await db.commit()
        await db.refresh(new_category)
        return new_category
    
    @staticmethod
    async def get_category_by_id(category_id: int, db: AsyncSession):
        category = await db.get(CategoryModel, category_id)
        
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
        return category
    
    @staticmethod
    async def update_category(category_id: int, category: CategorySchemaBase, db: AsyncSession):
        category_up = await CategoryService.get_category_by_id(category_id, db)

        category_dict = category.model_dump(exclude_unset=True)
        category_up.sqlmodel_update(category_dict)

        await db.commit()
        await db.refresh(category_up)
        return category_up

    @staticmethod
    async def delete_category(category_id: int, db: AsyncSession):
        category_del = await CategoryService.get_category_by_id(category_id, db)

        await db.delete(category_del)
        await db.commit()
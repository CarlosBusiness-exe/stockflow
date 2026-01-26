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
import pytest
from services.product_service import ProductService
from schemas.product_schema import ProductSchemaBase
from models.category_model import CategoryModel
from models.supplier_model import SupplierModel
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_create_product_sucess(db):
    category = CategoryModel(name="Tech")
    supplier = SupplierModel(name="Tec Info", cnpj="000.000.999-01", address="Rua a")
    db.add(category)
    db.add(supplier)
    await db.commit()
    await db.refresh(category)
    await db.refresh(supplier)

    product_data = ProductSchemaBase(
        name="Macbook",
        price=5400,
        qtd=5,
        category_id=category.id,
        supplier_id=supplier.id
    )

    new_product = await ProductService.create_product(product_data, db)

    assert new_product.id is not None
    assert new_product.name == "Macbook"
    assert new_product.category_id == category.id

@pytest.mark.asyncio
async def test_create_product_invalid_category(db):
    product_data = ProductSchemaBase(
        name="Macbook",
        price=5400,
        qtd=5,
        category_id=90, #Din't exist
        supplier_id=1
    )

    with pytest.raises(HTTPException) as exc:
        await ProductService.create_product(product_data, db)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Category not found."
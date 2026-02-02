import pytest
from fastapi import HTTPException
from services.product_service import ProductService
from schemas.product_schema import ProductSchemaCreate, ProductSchemaBase
from models.category_model import CategoryModel
from models.supplier_model import SupplierModel
from models.product_model import ProductModel

@pytest.mark.asyncio
async def test_create_product_success(db):
    category = CategoryModel(name="Bebidas")
    supplier = SupplierModel(name="Ambev", cnpj="123", address="Rua A")
    db.add_all([category, supplier])
    await db.commit()
    await db.refresh(category)
    await db.refresh(supplier)

    product_data = ProductSchemaCreate(
        name="Guaraná", price=5.0, qtd=10, 
        category_id=category.id, supplier_id=supplier.id
    )

    new_product = await ProductService.create_product(product_data, db)

    # Assert
    assert new_product.id is not None
    assert new_product.name == "Guaraná"
    assert new_product.category_id == category.id

@pytest.mark.asyncio
async def test_create_product_invalid_category(db):
    product_data = ProductSchemaCreate(
        name="Erro", price=1.0, qtd=1, category_id=999, supplier_id=1
    )

    with pytest.raises(HTTPException) as exc:
        await ProductService.create_product(product_data, db)
    
    assert exc.value.status_code == 404
    assert exc.value.detail == "Category not found."

@pytest.mark.asyncio
async def test_create_product_invalid_supplier(db):
    category = CategoryModel(name="Frios")
    db.add(category)
    await db.commit()
    await db.refresh(category)

    product_data = ProductSchemaCreate(
        name="Queijo", price=20.0, qtd=5, 
        category_id=category.id, supplier_id=999
    )

    with pytest.raises(HTTPException) as exc:
        await ProductService.create_product(product_data, db)
    
    assert exc.value.status_code == 404
    assert exc.value.detail == "Supplier not found."

@pytest.mark.asyncio
async def test_get_product_by_id_success(db):
    cat = CategoryModel(name="Limpeza")
    sup = SupplierModel(name="Omo", cnpj="456", address="Rua B")
    db.add_all([cat, sup])
    await db.commit()
    await db.refresh(cat)
    await db.refresh(sup)
    
    prod = ProductModel(name="Sabão", price=15.0, qtd=2, category_id=cat.id, supplier_id=sup.id)
    db.add(prod)
    await db.commit()
    await db.refresh(prod)

    # Act
    found_product = await ProductService.get_product_by_id(prod.id, db)

    # Assert
    assert found_product.id == prod.id
    assert found_product.name == "Sabão"

@pytest.mark.asyncio
async def test_get_product_by_id_not_found(db):
    with pytest.raises(HTTPException) as exc:
        await ProductService.get_product_by_id(999, db)
    
    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_update_product_success(db):
    cat = CategoryModel(name="Tech")
    sup = SupplierModel(name="Dell", cnpj="789", address="Rua C")
    db.add_all([cat, sup])
    await db.commit()
    await db.refresh(cat)
    await db.refresh(sup)
    
    prod = ProductModel(name="Mouse", price=50.0, qtd=10, category_id=cat.id, supplier_id=sup.id)
    db.add(prod)
    await db.commit()
    await db.refresh(prod)

    update_data = ProductSchemaCreate(
        name="Mouse Gamer", price=150.0, qtd=5, 
        category_id=cat.id, supplier_id=sup.id
    )

    updated = await ProductService.update_product(prod.id, update_data, db)

    assert updated.name == "Mouse Gamer"
    assert updated.price == 150.0

@pytest.mark.asyncio
async def test_delete_product_success(db):
    cat = CategoryModel(name="Teste")
    sup = SupplierModel(name="Teste", cnpj="1", address="1")
    db.add_all([cat, sup])
    await db.commit()
    await db.refresh(cat)
    await db.refresh(sup)
    
    prod = ProductModel(name="Deletar", price=1.0, qtd=1, category_id=cat.id, supplier_id=sup.id)
    db.add(prod)
    await db.commit()
    await db.refresh(prod)

    await ProductService.delete_product(prod.id, db)

    with pytest.raises(HTTPException) as exc:
        await ProductService.get_product_by_id(prod.id, db)
    assert exc.value.status_code == 404
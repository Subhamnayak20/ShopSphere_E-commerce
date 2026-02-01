from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from models import ProductModel
from schemas import ProductCreate, ProductResponse
from deps import get_db

app = FastAPI(title="Product Service")

from typing import List

@app.post("/products/add", response_model=list[ProductResponse])
def add_multiple_products(
    products: List[ProductCreate],
    db: Session = Depends(get_db)
):
    
    db_products = [ProductModel(**product.dict()) for product in products]
    db.add_all(db_products)
    db.commit()

    return db_products



# ➕ ADD product (COMMITTED)
# @app.post("/products", response_model=ProductResponse)
# def add_product(
#     product: ProductCreate,
#     db: Session = Depends(get_db)
# ):
#     db_product = ProductModel(**product.dict())
#     db.add(db_product)

#     db.commit()              # ✅ PERMANENT SAVE
#     db.refresh(db_product)   # get auto-generated ID

#     return db_product


# 📦 GET all + SEARCH
@app.get("/products", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()

@app.get("/products/search", response_model=list[ProductResponse])
def search_products(name:str, db: Session = Depends(get_db)):
    products = db.query(ProductModel).filter(
        ProductModel.name.ilike(f"%{name}%")
    ).all()

    if not products:
        return {"error": "Product not found"}

    return products




# ✏️ UPDATE product (COMMITTED)
@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    db_product = db.query(ProductModel).filter(
        ProductModel.id == product_id
    ).first()

    if not db_product:
        return {"error": "Product not found"}

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity

    db.commit()   # ✅ SAVE UPDATE

    return {"message": "Product updated successfully"}


# ❌ DELETE product (COMMITTED)
@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(ProductModel).filter(
        ProductModel.id == product_id
    ).first()

    if not product:
        return {"error": "Product not found"}

    db.delete(product)
    db.commit()   # ✅ SAVE DELETE

    return {"message": "Product deleted successfully"}









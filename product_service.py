# from fastapi import FastAPI, Depends
# from sqlalchemy.orm import Session

# from models import ProductModel
# from schemas import ProductCreate, ProductResponse
# from deps import get_db

# app = FastAPI(title="Product Service")

# from typing import List

# # multiple ADD products (COMMITTED)
# @app.post("/products/add", response_model=list[ProductResponse])
# def add_multiple_products(
#     products: List[ProductCreate],
#     db: Session = Depends(get_db)
# ):
    
#     db_products = [ProductModel(**product.dict()) for product in products]
#     db.add_all(db_products)
#     db.commit()

#     return db_products


# #  GET all SEARCH
# @app.get("/products", response_model=list[ProductResponse])
# def get_products(db: Session = Depends(get_db)):
#     return db.query(ProductModel).all()

# @app.get("/products/search", response_model=list[ProductResponse])
# def search_products(name:str, db: Session = Depends(get_db)):
#     products = db.query(ProductModel).filter(
#         ProductModel.name.ilike(f"%{name}%")
#     ).all()

#     if not products:
#         return {"error": "Product not found"}

#     return products

# @app.put("/products/{product_id}")
# def update_product(
#     product_id: int,
#     product: ProductCreate,
#     db: Session = Depends(get_db)
# ):
#     db_product = db.query(ProductModel).filter(
#         ProductModel.id == product_id
#     ).first()

#     if not db_product:
#         return {"error": "Product not found"}

#     db_product.name = product.name
#     db_product.description = product.description
#     db_product.price = product.price
#     db_product.quantity = product.quantity

#     db.commit()   # ✅ SAVE UPDATE

#     return {"message": "Product updated successfully"}


# # ❌ DELETE product (COMMITTED)
# @app.delete("/products/{product_id}")
# def delete_product(
#     product_id: int,
#     db: Session = Depends(get_db)
# ):
#     product = db.query(ProductModel).filter(
#         ProductModel.id == product_id
#     ).first()

#     if not product:
#         return {"error": "Product not found"}

#     db.delete(product)
#     db.commit()   # ✅ SAVE DELETE

#     return {"message": "Product deleted successfully"}


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from database import Base, engine
from models import Product
from schemas import ProductCreate, ProductResponse
from deps import get_db
from redis_db import redis_client

app = FastAPI(title="Product Service")

Base.metadata.create_all(bind=engine)

CACHE_TTL = 86400  # 24 hours
LIST_TTL = 300
SEARCH_TTL = 300

@app.post("/products", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    redis_client.setex(
        f"product:{db_product.id}",
        CACHE_TTL,
        json.dumps(
            ProductResponse.model_validate(db_product).model_dump()
        )
    )

    return db_product


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    cache_key = f"product:{product_id}"

    cached = redis_client.get(cache_key)
    if cached:
        print("⚡ Redis CACHE HIT")
        return json.loads(cached)

    print("🐌 Redis CACHE MISS")
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    redis_client.setex(
        cache_key,
        CACHE_TTL,
        json.dumps(
            ProductResponse.model_validate(product).model_dump()
        )
    )

    return product

@app.get("/products/search", response_model=list[ProductResponse])
def search_products(
    name: str,
    db: Session = Depends(get_db)
):
    name = name.strip().lower()
    if not name:
        return []

    cache_key = f"products:search:{name}"

    cached = redis_client.get(cache_key)
    if cached:
        print("⚡ Redis CACHE HIT → search")
        return json.loads(cached)

    print("🐌 Redis CACHE MISS → search")

    products = db.query(Product).filter(
        Product.name.ilike(f"%{name}%")
    ).all()

    # ❗ DO NOT cache empty results
    if products:
        redis_client.setex(
            cache_key,
            SEARCH_TTL,
            json.dumps([
                ProductResponse.model_validate(p).model_dump()
                for p in products
            ])
        )

    return products


@app.get("/products", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

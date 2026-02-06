from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel
from redis_db import redis
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Product Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Product(HashModel):
    name: str
    description: str = ""
    price: float
    quantity: int

    class Meta:
        database = redis

class ProductCreate(BaseModel):
    name: str
    description: str = ""
    price: float
    quantity: int

@app.get("/")
def root():
    return {"message": "Product Service is running"}

@app.post("/products/add")
def add_multiple_products(products: List[ProductCreate]):
    created_products = []
    for product in products:
        p = Product(**product.dict())
        p.save()
        created_products.append({
            "id": p.pk,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "quantity": p.quantity
        })
    return created_products

@app.get("/products")
def get_products():
    products = []
    for pk in Product.all_pks():
        p = Product.get(pk)
        products.append({
            "id": p.pk,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "quantity": p.quantity
        })
    return products

@app.get("/products/{product_id}")
def get_product(product_id: str):
    try:
        p = Product.get(product_id)
        return {
            "id": p.pk,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "quantity": p.quantity
        }
    except:
        raise HTTPException(status_code=404, detail="Product not found")

@app.get("/products/search")
def search_products(name: str):
    products = []
    for pk in Product.all_pks():
        p = Product.get(pk)
        if name.lower() in p.name.lower():
            products.append({
                "id": p.pk,
                "name": p.name,
                "description": p.description,
                "price": p.price,
                "quantity": p.quantity
            })
    return products

@app.put("/products/{product_id}")
def update_product(product_id: str, product: ProductCreate):
    try:
        p = Product.get(product_id)
        p.name = product.name
        p.description = product.description
        p.price = product.price
        p.quantity = product.quantity
        p.save()
        return {"message": "Product updated successfully"}
    except:
        raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
def delete_product(product_id: str):
    try:
        Product.delete(product_id)
        return {"message": "Product deleted successfully"}
    except:
        raise HTTPException(status_code=404, detail="Product not found")

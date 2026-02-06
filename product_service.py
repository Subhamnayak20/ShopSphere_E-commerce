import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

USE_REDIS = os.getenv("USE_REDIS", "true").lower() == "true"

if USE_REDIS:
    try:
        from redis_om import HashModel
        from redis_db import redis
    except Exception:
        # if import fails, fall back to in-memory
        USE_REDIS = False

from in_memory_db import InMemoryModel
from pydantic import BaseModel

class ProductSchema(BaseModel):
    name: str
    price: float
    quantity: int

app = FastAPI(title="Product Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if USE_REDIS:
    class Product(HashModel):
        name: str
        price: float
        quantity: int

        class Meta:
            database = redis
else:
    class Product(InMemoryModel):
        def __init__(self, name: str, price: float, quantity: int):
            super().__init__(name=name, price=price, quantity=quantity)

@app.get("/")
def root():
    return {"message": "Product Service is running"}

@app.post("/products")
def create_product(product: ProductSchema):
    if USE_REDIS:
        p = Product(**product.dict())
        p.save()
        # Convert redis_om model to dict for consistent output
        return {**product.dict(), "pk": p.pk}
    else:
        p = Product(product.name, product.price, product.quantity)
        p.save()
        return p.dict()

@app.get("/products")
def get_products():
    if USE_REDIS:
        # return list of dicts for consistency
        return [Product.get(pk) for pk in Product.all_pks()]
    return [p.dict() for p in Product.all()]

@app.get("/products/{pk}")
def get_product(pk: str):
    if USE_REDIS:
        return Product.get(pk)
    p = Product.get(pk)
    return p.dict() if p else None

@app.get("/products/search")
def search_products(name: str):
    if USE_REDIS:
        return Product.find(Product.name == name).all()
    return Product.find_by("name", name).all()

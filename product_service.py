from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid

app = FastAPI(title="Product Service")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database
products_db = {}

class ProductCreate(BaseModel):
    name: str
    description: str = ""
    price: float
    quantity: int

@app.get("/")
def root():
    return {"message": "Product Service is running", "status": "ok"}

@app.post("/products/add")
def add_multiple_products(products: List[ProductCreate]):
    created_products = []
    for product in products:
        product_id = str(uuid.uuid4())[:8]
        products_db[product_id] = {
            "id": product_id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "quantity": product.quantity
        }
        created_products.append(products_db[product_id])
    return created_products

@app.get("/products")
def get_products():
    return list(products_db.values())

@app.get("/products/search")
def search_products(name: str):
    results = [p for p in products_db.values() if name.lower() in p["name"].lower()]
    return results

@app.get("/products/{product_id}")
def get_product(product_id: str):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return products_db[product_id]

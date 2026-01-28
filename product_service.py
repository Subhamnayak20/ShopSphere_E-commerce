from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel
from redis_db import redis

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
    price: float
    quantity: int

    class Meta:
        database = redis

@app.get("/")
def root():
    return {"message": "Product Service is running"}

@app.post("/products")
def create_product(product: Product):
    product.save()
    return product

@app.get("/products")
def get_products():
    return Product.all_pks()

@app.get("/products/{pk}")
def get_product(pk: str):
    return Product.get(pk)

@app.get("/products/search")
def search_products(name: str):
    return Product.find(Product.name == name).all()

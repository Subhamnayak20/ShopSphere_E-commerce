from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel
from redis_db import redis
import requests

app = FastAPI(title="Order Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Order(HashModel):
    product_id: str
    quantity: int
    status: str = "PLACED"

    class Meta:
        database = redis

@app.get("/")
def root():
    return {"message": "Order Service is running"}

@app.post("/order")
def place_order(order: Order):
    if order.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be > 0")

    # Validate product exists and has enough quantity
    try:
        resp = requests.get(f"http://127.0.0.1:8000/products/{order.product_id}")
    except Exception:
        raise HTTPException(status_code=503, detail="Product service unavailable")

    if resp.status_code != 200:
        raise HTTPException(status_code=404, detail="Product not found")

    product = resp.json()
    if product.get("quantity", 0) < order.quantity:
        raise HTTPException(status_code=400, detail="Insufficient product quantity")

    order.save()
    return {
        "message": "Order placed successfully",
        "order_id": order.pk,
        "status": order.status
    }

@app.get("/orders")
def get_orders():
    return [Order.get(pk) for pk in Order.all_pks()]

@app.get("/orders/{pk}")
def get_order(pk: str):
    return Order.get(pk)

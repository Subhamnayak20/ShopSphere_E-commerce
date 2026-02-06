import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

USE_REDIS = os.getenv("USE_REDIS", "true").lower() == "true"
if USE_REDIS:
    try:
        from redis_om import HashModel
        from redis_db import redis
    except Exception:
        USE_REDIS = False

from in_memory_db import InMemoryModel
from pydantic import BaseModel

app = FastAPI(title="Order Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if USE_REDIS:
    class Order(HashModel):
        product_id: str
        quantity: int
        status: str = "PLACED"

        class Meta:
            database = redis
else:
    class Order(InMemoryModel):
        def __init__(self, product_id: str, quantity: int, status: str = "PLACED"):
            super().__init__(product_id=product_id, quantity=quantity, status=status)


class OrderSchema(BaseModel):
    product_id: str
    quantity: int

@app.get("/")
def root():
    return {"message": "Order Service is running"}

@app.post("/order")
def place_order(order_data: OrderSchema):
    if order_data.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be > 0")

    # Validate product exists and has enough quantity
    try:
        resp = requests.get(f"http://127.0.0.1:8000/products/{order_data.product_id}")
    except Exception:
        raise HTTPException(status_code=503, detail="Product service unavailable")

    if resp.status_code != 200:
        raise HTTPException(status_code=404, detail="Product not found")

    product = resp.json()
    if product.get("quantity", 0) < order_data.quantity:
        raise HTTPException(status_code=400, detail="Insufficient product quantity")

    if USE_REDIS:
        order = Order(**order_data.dict())
        order.save()
        return {
            "message": "Order placed successfully",
            "order_id": order.pk,
            "status": order.status
        }
    else:
        order = Order(order_data.product_id, order_data.quantity)
        order.save()
        return {
            "message": "Order placed successfully",
            "order_id": order.pk,
            "status": order.dict().get("status")
        }

@app.get("/orders")
def get_orders():
    if USE_REDIS:
        return [Order.get(pk) for pk in Order.all_pks()]
    return [o.dict() for o in Order.all()]

@app.get("/orders/{pk}")
def get_order(pk: str):
    o = Order.get(pk)
    return o.dict() if o and not USE_REDIS else o

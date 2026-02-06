from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel
from redis_db import redis
from pydantic import BaseModel
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

    order = Order(product_id=order_data.product_id, quantity=order_data.quantity)
    order.save()
    
    return {
        "message": "Order placed successfully",
        "order_id": order.pk,
        "status": order.status
    }

@app.get("/orders")
def get_orders():
    orders = []
    for pk in Order.all_pks():
        o = Order.get(pk)
        orders.append({
            "id": o.pk,
            "product_id": o.product_id,
            "quantity": o.quantity,
            "status": o.status
        })
    return orders

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    try:
        o = Order.get(order_id)
        return {
            "id": o.pk,
            "product_id": o.product_id,
            "quantity": o.quantity,
            "status": o.status
        }
    except:
        raise HTTPException(status_code=404, detail="Order not found")

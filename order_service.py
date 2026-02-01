from fastapi import FastAPI
from redis_om import HashModel
from redis_db import redis

app = FastAPI(title="Order Service")

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
    order.save()
    return {
        "message": "Order placed successfully",
        "order_id": order.pk,
        "status": order.status
    }

@app.get("/orders")
def get_orders():
    return Order.all_pks()

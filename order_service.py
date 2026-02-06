from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel
from redis_db import redis

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
    order.save()
    return {
        "message": "Order placed successfully",
        "order_id": order.pk,
        "status": order.status
    }

@app.get("/orders")
def get_orders():
    return Order.all_pks()

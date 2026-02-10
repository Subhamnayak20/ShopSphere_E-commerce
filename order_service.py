from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid

app = FastAPI(title="Order Service")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database
orders_db = {}

class OrderSchema(BaseModel):
    product_id: str
    product_name: str
    quantity: int

@app.get("/")
def root():
    return {"message": "Order Service is running", "status": "ok"}

@app.post("/order")
def place_order(order_data: OrderSchema):
    if order_data.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be > 0")

    order_id = str(uuid.uuid4())[:8]
    orders_db[order_id] = {
        "id": order_id,
        "product_id": order_data.product_id,
        "product_name": order_data.product_name,
        "quantity": order_data.quantity,
        "status": "PLACED"
    }
    
    return {
        "message": "Order placed successfully",
        "order_id": order_id,
        "status": "PLACED"
    }

@app.get("/orders")
def get_orders():
    return list(orders_db.values())

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]

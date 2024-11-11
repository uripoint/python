from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from datetime import datetime

app = FastAPI(title="Order Processing Service")

class OrderCreate(BaseModel):
    product_id: int
    quantity: int

class Order(OrderCreate):
    id: int
    timestamp: str

orders_db = {}
order_id_counter = 1

@app.get("/api/orders")
def list_orders():
    return list(orders_db.values())

@app.post("/api/orders")
def create_order(order: OrderCreate):
    global order_id_counter
    order_id = order_id_counter
    order_id_counter += 1
    
    new_order = {
        "id": order_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "timestamp": datetime.now().isoformat()
    }
    orders_db[order_id] = new_order
    return new_order

@app.get("/api/orders/{order_id}")
def get_order(order_id: int):
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Product Catalog Service")

class Product(BaseModel):
    name: str
    price: float
    description: str = None

products_db = {
    1: {
        "id": 1,
        "name": "Laptop",
        "price": 999.99,
        "description": "High-performance laptop"
    },
    2: {
        "id": 2,
        "name": "Smartphone",
        "price": 599.99,
        "description": "Latest model smartphone"
    }
}

@app.get("/api/products")
def list_products():
    return list(products_db.values())

@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    product = products_db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)

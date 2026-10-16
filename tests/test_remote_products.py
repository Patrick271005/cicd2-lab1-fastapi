import httpx2
from app.main import app
from app.product_client import get_product_fetcher

def fake_fetch_product(product_id: int) -> dict:
    return {"id": product_id, "name": "Laptop", "price": 899.0}

def provide_fake_product():
    return fake_fetch_product

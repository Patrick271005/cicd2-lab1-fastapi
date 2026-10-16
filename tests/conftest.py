import pytest 
from fastapi.testclient import TestClient

from app.main import app
from app.database import SessionLocal
from app.models import UserDB

@pytest.fixture(autouse=True)
def clear_users():
    with SessionLocal() as db:
        db.query(UserDB).delete()
        db.commit()

@pytest.fixture
def client():
    return TestClient(app)
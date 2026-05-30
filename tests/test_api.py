from fastapi.testclient import TestClient
from src.infrastructure.api import app
import src.infrastructure.api as api

client = TestClient(app)

class DummyPublisher:
    def publish_transaction(self, tx):
        return True

class FailingPublisher:
    def publish_transaction(self, tx):
        return False

def test_post_transaction_success(monkeypatch):
    monkeypatch.setattr(api.use_case, "publisher", DummyPublisher())
    
    response = client.post("/transactions", json={
        "amount": 50,
        "card_number": "1234567812345678",
        "restaurant_code": "R01"
    })
    
    assert response.status_code == 201
    assert "successfully" in response.json()["message"]

def test_post_transaction_invalid_data():
    response = client.post("/transactions", json={
        "amount": -50,
        "card_number": "123",
        "restaurant_code": "R01"
    })
    
    # Domain validation error translates to 400
    assert response.status_code == 400 

def test_post_transaction_server_error(monkeypatch):
    monkeypatch.setattr(api.use_case, "publisher", FailingPublisher())
    
    response = client.post("/transactions", json={
        "amount": 50,
        "card_number": "1234567812345678",
        "restaurant_code": "R01"
    })
    
    assert response.status_code == 500

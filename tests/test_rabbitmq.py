import pytest
from src.infrastructure.rabbitmq import RabbitMQPublisher
from src.core.entities import Transaction

class MockConnection:
    def __init__(self):
        self.closed = False
    
    def channel(self):
        return MockChannel()
        
    def close(self):
        self.closed = True

class MockChannel:
    def queue_declare(self, queue, durable):
        pass
        
    def basic_publish(self, exchange, routing_key, body, properties):
        pass

def test_publisher_success(monkeypatch):
    publisher = RabbitMQPublisher()
    
    # Mock the connection to avoid needing a real RabbitMQ
    monkeypatch.setattr(publisher, "get_connection", lambda: MockConnection())
    
    tx = Transaction(amount=150.0, card_number="1234567812345678", restaurant_code="REST1")
    result = publisher.publish_transaction(tx)
    
    assert result is True

def test_publisher_failure(monkeypatch):
    publisher = RabbitMQPublisher()
    
    def mock_fail():
        raise Exception("Connection failed")
        
    monkeypatch.setattr(publisher, "get_connection", mock_fail)
    
    tx = Transaction(amount=150.0, card_number="1234567812345678", restaurant_code="REST1")
    result = publisher.publish_transaction(tx)
    
    assert result is False

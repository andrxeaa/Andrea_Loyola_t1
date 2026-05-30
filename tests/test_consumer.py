import json
from src.consumer import RewardConsumer
from src.core.entities import Transaction

class MockChannel:
    def __init__(self):
        self.acked = False
        self.rejected = False
        self.requeued = False
        
    def basic_ack(self, delivery_tag):
        self.acked = True
        
    def basic_reject(self, delivery_tag, requeue):
        self.rejected = True
        self.requeued = requeue

class MockMethod:
    def __init__(self):
        self.delivery_tag = "tag123"

def test_consumer_callback_success():
    consumer = RewardConsumer()
    channel = MockChannel()
    method = MockMethod()
    
    tx = Transaction(amount=150.0, card_number="1234567812345678", restaurant_code="REST1")
    body = tx.json()
    
    consumer.callback(channel, method, None, body)
    
    # Verify ack was called
    assert channel.acked is True
    
    # Verify account was updated
    account = consumer.repository.get_account("1234567812345678")
    assert account.total_points == 15
    assert account.total_cashback == 3.0

def test_consumer_callback_failure():
    consumer = RewardConsumer()
    channel = MockChannel()
    method = MockMethod()
    
    # Invalid JSON body will trigger an exception
    body = "{"
    
    consumer.callback(channel, method, None, body)
    
    # Verify reject was called
    assert channel.rejected is True
    assert channel.requeued is False

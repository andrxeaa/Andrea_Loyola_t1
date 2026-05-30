import pytest
from src.core.entities import Transaction, CustomerAccount

def test_transaction_valid():
    tx = Transaction(amount=150.0, card_number="1234567812345678", restaurant_code="REST1")
    assert tx.amount == 150.0
    assert tx.card_number == "1234567812345678"

def test_transaction_invalid_amount():
    with pytest.raises(ValueError):
        Transaction(amount=-10, card_number="1234567812345678", restaurant_code="REST1")

def test_transaction_invalid_card():
    with pytest.raises(ValueError):
        Transaction(amount=100.0, card_number="123", restaurant_code="REST1")

def test_customer_account_defaults():
    account = CustomerAccount(card_number="1111222233334444")
    assert account.total_points == 0
    assert account.total_cashback == 0.0

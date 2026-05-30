import math
from typing import Protocol
from src.core.entities import Transaction, RewardCalculation, CustomerAccount

class MessagePublisher(Protocol):
    def publish_transaction(self, transaction: Transaction) -> bool:
        pass

class CustomerRepository(Protocol):
    def get_account(self, card_number: str) -> CustomerAccount:
        pass
    
    def save_account(self, account: CustomerAccount) -> None:
        pass

class RegisterDinnerUseCase:
    def __init__(self, publisher: MessagePublisher):
        self.publisher = publisher

    def execute(self, transaction_data: dict) -> Transaction:
        transaction = Transaction(**transaction_data)
        success = self.publisher.publish_transaction(transaction)
        if not success:
            raise Exception("Failed to publish transaction to broker")
        return transaction

class CalculateRewardsUseCase:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def execute(self, transaction_data: dict) -> RewardCalculation:
        transaction = Transaction(**transaction_data)
        
        # Calculate points: 1 point per 10 soles
        points = math.floor(transaction.amount / 10)
        
        # Calculate cashback: 2% of the amount
        cashback = round(transaction.amount * 0.02, 2)
        
        # Update account
        account = self.repository.get_account(transaction.card_number)
        account.total_points += points
        account.total_cashback += cashback
        self.repository.save_account(account)
        
        return RewardCalculation(
            transaction=transaction,
            points_earned=points,
            cashback_earned=cashback
        )

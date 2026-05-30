import pytest
from src.core.use_cases import RegisterDinnerUseCase, CalculateRewardsUseCase
from src.core.entities import Transaction
from src.infrastructure.repository import InMemoryCustomerRepository

class MockPublisher:
    def __init__(self, should_succeed=True):
        self.should_succeed = should_succeed
        self.published = False
    
    def publish_transaction(self, tx: Transaction) -> bool:
        self.published = True
        return self.should_succeed

def test_register_dinner_success():
    publisher = MockPublisher(should_succeed=True)
    use_case = RegisterDinnerUseCase(publisher)
    
    data = {"amount": 200, "card_number": "1111222233334444", "restaurant_code": "R1"}
    tx = use_case.execute(data)
    
    assert tx.amount == 200
    assert publisher.published is True

def test_register_dinner_fail():
    publisher = MockPublisher(should_succeed=False)
    use_case = RegisterDinnerUseCase(publisher)
    
    data = {"amount": 200, "card_number": "1111222233334444", "restaurant_code": "R1"}
    with pytest.raises(Exception, match="Failed to publish"):
        use_case.execute(data)

def test_calculate_rewards():
    repo = InMemoryCustomerRepository()
    use_case = CalculateRewardsUseCase(repo)
    
    data = {"amount": 155.0, "card_number": "1111222233334444", "restaurant_code": "R1"}
    result = use_case.execute(data)
    
    assert result.points_earned == 15
    assert result.cashback_earned == 3.10
    
    account = repo.get_account("1111222233334444")
    assert account.total_points == 15
    assert account.total_cashback == 3.10

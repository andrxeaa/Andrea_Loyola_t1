from src.core.entities import CustomerAccount
from src.core.use_cases import CustomerRepository

class InMemoryCustomerRepository(CustomerRepository):
    def __init__(self):
        self.db = {}

    def get_account(self, card_number: str) -> CustomerAccount:
        if card_number not in self.db:
            self.db[card_number] = CustomerAccount(card_number=card_number)
        return self.db[card_number]

    def save_account(self, account: CustomerAccount) -> None:
        self.db[account.card_number] = account

from datetime import datetime
from pydantic import BaseModel, Field

class Transaction(BaseModel):
    amount: float = Field(..., gt=0, description="Monto consumido")
    card_number: str = Field(..., min_length=16, max_length=16, description="Número de tarjeta del cliente")
    restaurant_code: str = Field(..., description="Código del restaurante afiliado")
    transaction_date: datetime = Field(default_factory=datetime.now, description="Fecha y hora de la transacción")

class RewardCalculation(BaseModel):
    transaction: Transaction
    points_earned: int
    cashback_earned: float

class CustomerAccount(BaseModel):
    card_number: str
    total_points: int = 0
    total_cashback: float = 0.0

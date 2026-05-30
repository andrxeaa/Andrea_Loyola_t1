from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.core.use_cases import RegisterDinnerUseCase
from src.infrastructure.rabbitmq import RabbitMQPublisher

app = FastAPI(title="Restaurant Rewards API")

publisher = RabbitMQPublisher()
use_case = RegisterDinnerUseCase(publisher)

class TransactionRequest(BaseModel):
    amount: float
    card_number: str
    restaurant_code: str

@app.post("/transactions", status_code=201, responses={400: {"description": "Bad Request"}, 500: {"description": "Server Error"}})
def register_transaction(request: TransactionRequest):
    try:
        transaction = use_case.execute(request.dict())
        return {
            "message": "Transaction registered successfully and sent to processing",
            "transaction_date": transaction.transaction_date
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error while processing transaction")

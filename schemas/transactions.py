from pydantic import BaseModel

class Transaction(BaseModel):
    amount: float
    type: str
    category: str
    note: str = ""
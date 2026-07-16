from pydantic import BaseModel
from datetime import datetime
class Transaction(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: datetime
    note: str = ""

class Budget(BaseModel):
    budget: float
    feeding: float
    airtime_data: float
    electricity: float
    betting: float
    transfer: float

class Savings(BaseModel):
    name: str
    target_amount: float
    deadline: str

class Contribution(BaseModel):
    amount: float
    date: datetime

class MonthlyReport(BaseModel):
    month: int

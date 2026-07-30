from pydantic import BaseModel
from datetime import datetime

class Savings(BaseModel):
    name: str
    target_amount: float
    deadline: str

class Contribution(BaseModel):
    amount: float
    date: datetime
    savings_name: str

class SavingsPlan(BaseModel):
    saving_plan: str
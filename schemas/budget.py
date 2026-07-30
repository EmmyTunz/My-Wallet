from pydantic import BaseModel

class Budget(BaseModel):
    budget: float
    feeding: float
    airtime_data: float
    electricity: float
    betting: float
    transfer: float

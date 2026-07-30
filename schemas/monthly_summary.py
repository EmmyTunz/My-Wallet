from pydantic import BaseModel

class MonthlyReport(BaseModel):
    month: int
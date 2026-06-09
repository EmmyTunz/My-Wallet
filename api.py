from transaction import *
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title= "Personal Finance Tracker")

class Transaction(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: datetime
    note: str = ""

# Add a new transaction
@app.post("/transaction/new")
def create_transaction(tx: Transaction):
    data = load_data()
    result = add_transaction(amount=tx.amount, transaction_type=tx.type, category=tx.category, note=tx.note, date=tx.date)
    save_data(result)
    if data == result:
        raise HTTPException(status_code=501, detail= "Please specify the transaction type; Expense or Income")
    else:
        return {"message": "Transaction added successfully"}


# Display all transactions
@app.get("/transaction", summary="Load all transactions")
def get_transaction():
    data = load_data()
    return data



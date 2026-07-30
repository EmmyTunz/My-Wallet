from fastapi import APIRouter, HTTPException
from services.transactions_services.transaction import *
from schemas.transactions import Transaction

router = APIRouter()

#Get all transactions
@router.get("/transaction", summary="Load all transactions")
def get_transaction():
        data = load_data()
        return data

#Add new transaction
@router.post("/transaction/new")
def create_transaction(tx: Transaction):
    data = load_data()
    result = add_transaction(amount=tx.amount, transaction_type=tx.type, category=tx.category, note=tx.note)
    save_data(result)
    if data == result:
        raise HTTPException(status_code=501, detail= "Please specify the transaction type; Expense or Income")
    else:
        return {"message": "Transaction added successfully"}


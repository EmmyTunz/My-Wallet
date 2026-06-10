from budget_tracker import new_budget, get_budget
from transaction import *
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from expenses import check_expenses


app = FastAPI(title= "Personal Finance Tracker")

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

# create / check budget and category limits
@app.post("/budget/new", summary= "Create budget limits")
def create_budget(bd: Budget):
    set_budget = new_budget(budget=bd.budget, feeding=bd.feeding, airtime_data=bd.airtime_data, electricity=bd.electricity, betting=bd.betting, transfer=bd.transfer)
    return set_budget
# View budget limits
@app.get("/budget", summary="View Budget limits")
def view_budget():
    budget = get_budget()
    return budget
# compare category limits with expenses
@app.get("/budget/category_limits", summary="Check category limits")
def check_limits():
    trans_list = get_transaction()
    budget_data = get_budget()
    expenses_check = check_expenses(transaction_list=trans_list, budget_file=budget_data)
    return expenses_check




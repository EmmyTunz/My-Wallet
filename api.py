from all_services.budget_services.budget_tracker import new_budget, get_budget, check_budget
from all_services.transactions_services.transaction import *
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from all_services.expenses_services.expenses import check_expenses, total_expenses, expenses_list_func, calculate_categories
from all_services.savings_services.savings_tracker import *
from all_services.Monthly_summary.monthly_summary import *
from all_services.balance_services.balance import *
from all_services.income_services.income import calculate_total_income

app = FastAPI(title= "Personal Finance Tracker")

class Transaction(BaseModel):
    amount: float
    type: str
    category: str
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

# Display Balance, total_income
@app.get("/balance", summary="Display current balance")
def display_balance():
    current_balance = BalanceTracker()
    return current_balance.display_balance()

@app.get("/total_income", summary="Display total income")
def display_total_income():
    transaction_list = load_data()
    total_income = calculate_total_income(transaction_list=transaction_list)
    return total_income

@app.get("/total_expenses", summary="Display total expenses")
def display_total_expenses():
    transaction_list = load_data()
    total_expenditure = total_expenses(transaction_list=transaction_list)
    return total_expenditure


# Add a new transaction
@app.post("/transaction/new")
def create_transaction(tx: Transaction):
    data = load_data()
    result = add_transaction(amount=tx.amount, transaction_type=tx.type, category=tx.category, note=tx.note)
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
    set_budget = new_budget(budget=bd.budget, feeding=bd.feeding, airtime_data=bd.airtime_data, electricity=bd.electricity,
                            betting=bd.betting, transfer=bd.transfer)
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
    expenses_list = expenses_list_func(trans_list)
    expenses_amount = total_expenses(transaction_list=trans_list)
    budget_check = check_budget(budget_dict=budget_data, total_expenses= expenses_amount)
    expenses_check = check_expenses(expenses_list=expenses_list, budget_file=budget_data)
    return budget_check, expenses_check


# Savings Tracker

## - create savings
@app.post("/savings/new", summary="Create new savings")
def new_savings(sn: Savings):
    savings_new = create_savings(name=sn.name, target_amount=sn.target_amount, deadline=sn.deadline)
    return savings_new

## - view savings
@app.get("/savings", summary="View savings")
def view_savings():
    load = load_savings()
    return load

## - log savings
@app.post("/savings/log", summary="Add to savings")
def log_savings(cd: Contribution):
    savings_data = load_savings()
    contribution_log = log_contributions(savings_data, cd.amount, cd.date)
    return contribution_log

## - find out amount remaining to reach saving goal
@app.get("/savings/amount_remaining", summary="find out how much is left till savings goal")
def amount_remaining():
    savings_data = load_savings()
    calculate_amount = calculate_amount_remaining(savings_data)
    return calculate_amount

## - find out how many days left to reach goal
@app.get("/savings/days_left", summary="find out how many days left to reach goal")
def days_left():
    data = load_savings()
    days_l = days_remaining(data)
    return {"message": f"you have {days_l} days left to reach your savings goal"}

## - find out much to save per day
@app.get("/savings/amount_per_day", summary="find out much to save per day")
def savings_per_day():
    data = load_savings()
    amount = amount_per_day(data)
    return {"message": f"You have to save N{amount:.2f} everyday to reach your goal"}


# Monthly Summary
## - Generate Monthly summary for any given month
@app.post("/monthly_summary", summary="Request Monthly summary for a specified month")
def generate_report(mr: MonthlyReport):
    savings_data = load_savings()
    trans_data = load_data()

    monthly_transaction_list = arrange_transaction_data(transaction_list=trans_data, month=mr.month)
    total_income = calculate_total_income(monthly_transaction_list)

    expense_list = expenses_list_func(transaction_list=monthly_transaction_list)
    total_expense = total_expenses(transaction_list=expense_list)

    net_balance = total_income - total_expense

    biggest_expense = biggest_expense_func(expense_list)

    categories_list = calculate_categories(expense_list)
    top_categories = check_top_categories(categories_list)

    savings_data_list = get_savings_data(savings_data, mr.month)
    savings_rate = calculate_savings_rate(savings_data_list, total_income)

    generate_monthly_report = create_monthly_report(total_income, total_expense, net_balance, top_categories, biggest_expense, savings_rate)
    return generate_monthly_report

## - view the generated report
@app.get("/monthly_summary/view", summary="View generated report")
def view_report():
    report = get_report()
    return report



from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


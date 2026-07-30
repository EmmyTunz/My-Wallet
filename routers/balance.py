from fastapi import APIRouter
from services.transactions_services.transaction import load_data
from services.balance_services.balance import BalanceTracker
from services.expenses_services.expenses import total_expenses
from services.Monthly_summary.monthly_summary import calculate_total_income

router = APIRouter()

# Display Balance, total_income
@router.get("/balance", summary="Display current balance")
def display_balance():
    current_balance = BalanceTracker()
    return current_balance.display_balance()

@router.get("/total_income", summary="Display total income")
def display_total_income():
    transaction_list = load_data()
    total_income = calculate_total_income(transaction_list)
    return total_income

@router.get("/total_expenses", summary="Display total expenses")
def display_total_expenses():
    transaction_list = load_data()
    total_expenditure = total_expenses(transaction_list=transaction_list)
    return total_expenditure

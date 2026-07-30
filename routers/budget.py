from fastapi import APIRouter
from services.budget_services.budget_tracker import *
from services.transactions_services.transaction import load_data
from services.expenses_services.expenses import expenses_list_func, total_expenses, check_expenses
from schemas.budget import Budget

router = APIRouter()

#Create New Budget and category Limits
@router.post("/budget/new", summary= "Create budget limits")
def create_budget(bd: Budget):
    set_budget = new_budget(budget=bd.budget, feeding=bd.feeding, airtime_data=bd.airtime_data, electricity=bd.electricity,
                            betting=bd.betting, transfer=bd.transfer)
    return set_budget

#Display Budget and Category Limits
@router.get("/budget", summary="View Budget limits")
def view_budget():
    budget = get_budget()
    return budget

# compare category limits with expenses
@router.get("/budget/category_limits", summary="Check category limits")
def check_limits():
    trans_list = load_data()
    budget_data = get_budget()
    expenses_list = expenses_list_func(trans_list)
    expenses_amount = total_expenses(transaction_list=trans_list)
    budget_check = check_budget(budget_dict=budget_data, total_expenses= expenses_amount)
    expenses_check = check_expenses(expenses_list=expenses_list, budget_file=budget_data)
    return budget_check, expenses_check
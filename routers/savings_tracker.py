from fastapi import APIRouter
from services.savings_services.savings_tracker import *
from schemas.savings_tracker import Savings, Contribution, SavingsPlan

router = APIRouter()

## - create savings
@router.post("/savings/new", summary="Create new savings")
def new_savings(sn: Savings):
    savings_new = create_savings(name=sn.name, target_amount=sn.target_amount, deadline=sn.deadline)
    return savings_new

## - view savings
@router.get("/savings", summary="View savings")
def view_savings():
    load = load_savings()
    return load

## - log savings
@router.post("/savings/log", summary="Add to savings")
def log_savings(cd: Contribution):
    contribution_log = log_contributions(cd.amount, cd.date, cd.savings_name)
    return contribution_log

@router.post("/savings/amount_remaining", summary="find out how much is left till savings goal")
def amount_remaining(sp: SavingsPlan):
    calculate_amount = calculate_amount_remaining(sp.saving_plan)
    return calculate_amount

## - find out how many days left to reach goal
@router.post("/savings/days_left", summary="find out how many days left to reach goal")
def days_left(sp: SavingsPlan):
    days_l = days_remaining(sp.saving_plan)
    if isinstance(days_l, int):
        return {"message": f"you have {days_l} days left to reach your savings goal"}
    else:
        return days_l

## - find out much to save per day
@router.post("/savings/amount_per_day", summary="find out much to save per day")
def savings_per_day(sp: SavingsPlan):
    amount = amount_per_day(sp.saving_plan)
    return {"message": f"You have to save N{amount:.2f} everyday to reach your goal"}
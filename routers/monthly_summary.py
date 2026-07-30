from fastapi import APIRouter
from services.Monthly_summary.monthly_summary import *
from services.transactions_services.transaction import load_data
from services.savings_services.savings_tracker import load_savings
from services.expenses_services.expenses import *
from schemas.monthly_summary import MonthlyReport

router = APIRouter()

# Monthly Summary
## - Generate Monthly summary for any given month
@router.post("/monthly_summary", summary="Request Monthly summary for a specified month")
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
@router.get("/monthly_summary/view", summary="View generated report")
def view_report():
    report = get_report()
    return report
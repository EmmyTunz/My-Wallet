import json
import os
from datetime import datetime
# View report for each month

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

## - gather all transaction from a single month into one list
def arrange_transaction_data(transaction_list, month):
    monthly_transaction_list = []
    for i in transaction_list:
        if datetime.strptime(i["Transaction"]["date"], "%d/%m/%Y %H:%M").month == month:
            monthly_transaction_list.append(i)

    return monthly_transaction_list

## - calculate the total income in that month
def calculate_total_income(monthly_report_list):
    income_amount = 0
    for a in monthly_report_list:
        if a["Transaction"]["type"] == "Income":
            income_amount += a["Transaction"]["amount"]
    return income_amount

## - get the biggest expense for the month
def biggest_expense_func(expenses_list):
    expenses_list.sort(key=lambda x: x["Transaction"]["amount"])
    top_expenses_list = expenses_list
    return top_expenses_list[len(expenses_list)-1]

## - get the top 3 spending categories
def check_top_categories(categories_list):
    categories_total_amount_dict = {
        "feeding_amount": categories_list[0],
        "airtime_data_amount": categories_list[1],
        "electricity_amount": categories_list[2],
        "betting_amount": categories_list[3],
        "transfer_amount": categories_list[4],
    }
    sort_categories_dict = dict(sorted(categories_total_amount_dict.items(), key=lambda x: x[1], reverse=True))
    top_3_categories = dict(list(sort_categories_dict.items())[:3])
    return top_3_categories


## - get savings data for the month
def get_savings_data(savings_data, month):
    savings_data_list = []
    for i in savings_data["contributions"]:
        if datetime.strptime(i["date"], "%d/%m/%Y %H:%M").month == month:
            savings_data_list.append(i)
    return savings_data_list


## - calculate the savings rate for the month
def calculate_savings_rate(savings_data_list, total_income):
    amount = 0
    for i in savings_data_list:
        amount += i["amount"]
    savings_rate = amount/total_income * 100
    return savings_rate

## - generate and save full monthly report
def create_monthly_report(total_income, total_expenses, net_balance, top_categories, biggest_expense, savings_rate):
    monthly_report = {
        "total_income": total_income,
        "total_expense": total_expenses,
        "net_balance": net_balance,
        "top_categories": top_categories,
        "biggest_expense": biggest_expense,
        "savings_rate": savings_rate,
    }
    with open(os.path.join(BASE_DIR, "monthly_report.txt"), "w") as data:
        json.dump(monthly_report, data, indent=2)

    return {"message": "Monthly report has been generated"}

## - get generated report
def get_report():
    try:
        with open(os.path.join(BASE_DIR, "monthly_report.txt"), "r") as data:
            report = json.load(data)
        return report

    except FileNotFoundError:
        return {"message": "You have not requested a report yet"}
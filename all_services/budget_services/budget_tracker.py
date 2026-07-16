import json
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class BudgetTracker:
    def __init__(self):
        self.feeding_limit = int(input("Enter your monthly feeding budget "))
        self.airtime_data_limit = int(input("Enter your Monthly Airtime/Data limit "))
        self.electricity_limit = int(input("Enter your Monthly electricity limit "))
        self.betting_limit = int(input("Enter your monthly betting limit "))
        self.transfer_limit = int(input("Enter your monthly transfer limit "))
        self.budget = (self.transfer_limit + self.betting_limit + self.feeding_limit + self.electricity_limit +
                       self.airtime_data_limit)


    def save_budget_data(self):
        new_budget(budget=self.budget, feeding=self.feeding_limit, airtime_data=self.airtime_data_limit, electricity=self.electricity_limit,
                   betting=self.betting_limit, transfer=self.transfer_limit)


def new_budget(budget, feeding, airtime_data, electricity, betting, transfer):
    if os.path.exists(os.path.join(BASE_DIR, "budget_limits.txt")):
        return {"Message" : "You have budget limits already, view or edit them"}
    else:
        budget_limit_dict = {
            "budget": budget,
            "feeding": feeding,
            "airtime/data": airtime_data,
            "electricity": electricity,
            "betting": betting,
            "transfer": transfer,
        }

        with open("budget_limits.txt", "w") as data:
            json.dump(budget_limit_dict, data)
        return {"message": "Budgets set successfully!"}

def get_budget():
    try:
        with open(os.path.join(BASE_DIR, "budget_limits.txt"), "r") as budget_data:
            budget_file = json.load(budget_data)
            return budget_file
    except FileNotFoundError:
        return {"message": "You have not set your budget limits yet"}

def check_category_limits(limit, category_amount, budget_dict):
    if budget_dict[limit] <= category_amount:
        return {"message" : f"You have exceeded your monthly {limit}, you spent a total of N{category_amount}"}
    else:
        return {"message": f"You still have N{budget_dict[limit] - category_amount} for {limit} to spend"}


def check_budget(budget_dict, total_expenses):
    amount_remaining = budget_dict["budget"] - total_expenses
    if total_expenses >= (80/100) * budget_dict["budget"]:
        return {"message": f"You have now spent at least 80%; N{total_expenses} of your budget, N{amount_remaining} left."}
    else:
        return {"message": f"N{total_expenses} spent, You are still within your budget and you have {amount_remaining} left"}









from datetime import datetime, date
import json
import os
import pandas as pd
from all_services.balance_services.balance import BalanceTracker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
balance = BalanceTracker()

## Load saving goals data from savings.json
def load_savings():
    savings_goal_list = []
    try:
        with open(os.path.join(BASE_DIR, "savings.json"), "r") as data:
            savings_data = json.load(data)
            for key in savings_data["saving_goals"]:
                goal = savings_data["saving_goals"][key]
                savings_goal_list.append({
                    "saving_goals": {
                    "name": goal["name"],
                    "target_amount": goal["target_amount"],
                    "deadline": goal["deadline"],
                    "contributions": goal["contributions"]
                }})
        return savings_goal_list
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return savings_goal_list

## create new saving goal
def create_savings(name, target_amount, deadline):
    saving_goals_data = load_savings()
    savings_data = {
        "saving_goals": {
            "name": name,
            "target_amount": target_amount,
            "deadline": deadline,
            "contributions": []
        }
    }
    saving_goals_data.append(savings_data)
    save_savings_data(saving_goals_data)
    return {"message": "Savings goal created successfully."}

## save savings data to savings.json
def save_savings_data(data):
    data = pd.DataFrame(data)
    data.to_json(os.path.join(BASE_DIR, "savings.json"))

## add money to individual saving goal
def log_contributions(amount, date_log, saving_goal_name):
    saving_goals_data = load_savings()
    for i in saving_goals_data:
        saving_goal = i["saving_goals"]
        if saving_goal["name"] == saving_goal_name:
            if amount > 0:
                contribution = {
                    "amount" : amount,
                    "date" : date_log.strftime("%d/%m/%Y %H:%M")
                }
                saving_goal["contributions"].append(contribution)
                save_savings_data(saving_goals_data)
                balance.remove_savings_from_balance(amount)
                balance.save_balance()
                return {"message": f"Good Job! you just added N{amount} to {saving_goal["name"]}."}
            break
        else:
            pass
    return None


def calculate_amount_remaining(savings_data):
    amount = 0
    for i in savings_data["contributions"]:
        amount += i["amount"]
    amount_remaining = savings_data["target_amount"] - amount
    return amount_remaining

def days_remaining(savings_data):
    deadline = datetime.strptime(savings_data["deadline"], "%d/%m/%Y").date()
    today = date.today()
    days_left = (deadline - today).days
    return days_left

def amount_per_day(savings_data):
    total_amount = savings_data["target_amount"]
    no_of_days = days_remaining(savings_data)
    amount_day = total_amount / no_of_days
    return amount_day





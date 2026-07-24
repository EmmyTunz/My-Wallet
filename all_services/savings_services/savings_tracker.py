from datetime import datetime, date
import json
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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

def save_savings_data(data):
    data = pd.DataFrame(data)
    data.to_json(os.path.join(BASE_DIR, "savings.json"))

def log_contributions(savings_data, amount, date_log):
    contribution = {
        "amount" : amount,
        "date" : date_log.strftime("%d/%m/%Y %H:%M")
    }
    savings_data["contributions"].append(contribution)
    with open(os.path.join(BASE_DIR, "savings.json"), "w") as data:
        json.dump(savings_data, data, indent=4)

    return {"message": f"Good Job! you just saved N{amount}."}

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





from datetime import datetime, date
import json

def create_savings(name, target_amount, deadline):
    savings_data = {
        "name": name,
        "target_amount": target_amount,
        "deadline": deadline,
        "contributions": []
    }
    with open("savings.json", "w") as data:
        json.dump(savings_data, data, indent=4)

    return {"message": "Savings goal created successfully."}


def load_savings():
    try:
        with open("savings.json") as data:
            savings_data = json.load(data)
        return savings_data
    except FileNotFoundError:
        return {"message" : "You have no savings, create one"}

def log_contributions(savings_data, amount, date_log):
    contribution = {
        "amount" : amount,
        "date" : date_log.strftime("%d/%m/%Y %H:%M")
    }
    savings_data["contributions"].append(contribution)
    with open("savings.json", "w") as data:
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





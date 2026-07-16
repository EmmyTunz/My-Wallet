from datetime import datetime
from all_services.balance_services.balance import BalanceTracker
import pandas as pd
import json

balance = BalanceTracker()

def load_data():
    transaction_list = []
    try:
        with open("Transaction.json", "r") as data_file:
            transaction_file = json.load(data_file)
            for key in transaction_file["Transaction"]:
                key = transaction_file["Transaction"][key]
                transaction_list.append({
                    "Transaction": {
                        "id": key["id"],
                        "amount": key["amount"],
                        "type": key["type"],
                        "category": key["category"],
                        "date": key["date"],
                        "note": key["note"],
                    }})
        return transaction_list

    except FileNotFoundError, json.decoder.JSONDecodeError:
        transaction_list = []
        return transaction_list

def add_transaction(amount, transaction_type, category, note, date=datetime.now()):
    data = load_data()
    transaction_dict = {
                "Transaction": {
                    "id": data[len(data) - 1]["Transaction"]["id"] + 1,
                    "amount" : amount,
                    "type" : transaction_type,
                    "category": category,
                    "date" : date.strftime("%d/%m/%Y %H:%M"),
                    "note" : note,
                }
            }
    update = balance.update_balance(new_transaction=transaction_dict)
    balance.save_balance()
    if update:
        data.append(transaction_dict)
    return data

def save_data(data):
    data = pd.DataFrame(data)
    data.to_json("Transaction.json")



# def del_transaction(transaction_id):
#     data = load_data()


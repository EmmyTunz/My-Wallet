import pandas as pd
import json
from datetime import datetime

new_transaction = True
transaction_list = []



try:
    with open("Transaction.json", "r") as data_file:
        transaction_file = json.load(data_file)
        print(transaction_file)
        for key in transaction_file["Transaction"]:
            key = transaction_file["Transaction"][key]
            transaction_list.append({
                "Transaction": {
                    "amount" : key["amount"],
                    "type" : key["type"],
                    "date" : key["date"],
                    "note" : key["note"],
        }})
        print(transaction_list)

except FileNotFoundError:
    transaction_list = []



while new_transaction:
    transaction_amount = int(input("Enter Transaction Amount in digits "))
    transaction_type = input("Enter Transaction Type Income/Expense ")
    category = input("Enter the Category of this transaction ")
    date = datetime.now()
    note = input("Enter a description ")
    new_transaction = input("New transaction? (True/False) ")
    if new_transaction == "False":
        new_transaction = False

    transaction_dict = {
        "Transaction": {
            "amount" : transaction_amount,
            "type" : transaction_type,
            "date" : date,
            "note" : note,
        }
    }
    transaction_list.append(transaction_dict)
data = pd.DataFrame(transaction_list)
data.to_json("Transaction.json")
print(transaction_list)
print(data)


# add transaction to table
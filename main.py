import pandas as pd
import json
from datetime import datetime
from prettytable import PrettyTable
from budget_tracker import BudgetTracker

# Load existing data from previous sessions.
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
        # get the transaction ID of the previous transaction and add 1 to it for the next transaction
        transaction_id = int(
            list(transaction_file["Transaction"].keys())[len(transaction_file["Transaction"].keys()) - 1]) + 1

except FileNotFoundError, json.decoder.JSONDecodeError:
    transaction_list = []
    transaction_id = 0




# ask the user what they want to do
user_input = input("What would you like to do? enter add(to add a new transaction), set(to set your monthly budget),"
                   " view(to view transactions and track your budget" ).lower()


if user_input == "add":
    new_transaction = True
    # add new transaction to table
    while new_transaction:
        transaction_amount = int(input("Enter Transaction Amount in digits "))
        transaction_type = input("Enter Transaction Type Income/Expense ").capitalize()
        category = input("Enter the Category of this transaction ").capitalize()
        date = datetime.now()
        note = input("Enter a description ")

        transaction_dict = {
            "Transaction": {
                "id": transaction_id,
                "amount" : transaction_amount,
                "type" : transaction_type,
                "category": category,
                "date" : date.strftime("%d/%m/%Y %H:%M"),
                "note" : note,
            }
        }
        transaction_list.append(transaction_dict)

        new_transaction = input("New transaction? (True/False) ").capitalize()
        if new_transaction == "False":
            new_transaction = False
        elif new_transaction == "True":
            new_transaction = "True"
            transaction_id += 1
        else:
            new_transaction = input("is there a new transaction? type True or False ").capitalize()
    data = pd.DataFrame(transaction_list)
    data.to_json("Transaction.json")

# user_input = set.
elif user_input == "set":
    budget_tracker = BudgetTracker()
    budget_limit_dict = {
        "budget": budget_tracker.budget,
        "feeding": budget_tracker.feeding_limit,
        "airtime/data": budget_tracker.airtime_data_limit,
        "electricity": budget_tracker.electricity_limit,
        "betting": budget_tracker.betting_limit,
        "transfer": budget_tracker.transfer_limit,
    }
    # save budget data
    with open("budget_limits.txt", "w") as data:
        json.dump(budget_limit_dict, data)



# user_input = view.
elif user_input == "view":
    # Display Transaction Table
    print(transaction_list)
    transaction_table = PrettyTable(["Transaction_ID", "Amount", "Type", "Category", "Date", "Note"])
    for i in transaction_list:
        transaction_table.add_row([i["Transaction"]["id"], i["Transaction"]["amount"], i["Transaction"]["type"], i["Transaction"]["category"], i["Transaction"]["date"], i["Transaction"]["note"]])
    print(transaction_table)

    # get budget data
    try:
        with open("budget_limits.txt", "r") as budget_data:
            budget_file = json.load(budget_data)
    except FileNotFoundError:
        print("You have not set your Budget or Limits yet")




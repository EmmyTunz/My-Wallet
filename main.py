import pandas as pd
import json
import os.path
from datetime import datetime
from prettytable import PrettyTable
from budget_tracker import BudgetTracker, check_budget, check_category_limits
from balance import BalanceTracker


# Load balance
balance = BalanceTracker()


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
    print("Welcome to My wallet!\nstart by setting your budget for the month")



user_continue = True

while user_continue:
    # ask the user what they want to do
    user_input = input("What would you like to do? enter add(to add a new transaction), set(to set your monthly budget),"
                       " view(to view transactions and track your budget \n").lower()


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

            # update balance and save
            update = balance.update_balance(new_transaction=transaction_dict)
            balance.save_balance()

            balance.display_balance()
            if update:
                transaction_list.append(transaction_dict)
            else:
                print("Enter a valid Transaction (i) ensure Income/Expense is spelt correctly or ii) Fund your wallet")


            new_transaction = input("New transaction? (True/False) ").capitalize()
            if new_transaction == "False":
                new_transaction = False
            elif new_transaction == "True":
                new_transaction = True
                transaction_id += 1
            else:
                new_transaction = input("is there a new transaction? type True or False ").capitalize()
                if new_transaction == "False":
                    new_transaction = False

        data = pd.DataFrame(transaction_list)
        data.to_json("Transaction.json")

        new_input = input("Quit Program? y/n ").lower()
        if new_input == "y":
            user_continue = False
            print("Exiting....")

    # user_input = set.
    elif user_input == "set":
        if os.path.exists("budget_limits.txt"):
            print("You have already set your limits")
            user_input = input("Do you want to reset it? y/n ").lower()
            if user_input == "y":
                budget_tracker = BudgetTracker()
                budget_tracker.save_budget_data()
        else:
            budget_tracker = BudgetTracker()
            budget_tracker.save_budget_data()

        new_input = input("Quit Program? y/n ").lower()
        if new_input == "y":
            user_continue = False
            print("Exiting....")


    # user_input = view.
    elif user_input == "view":
        # Display  available balance
        print(f"Balance: N{balance.balance}")
        # Display Transaction Table
        transaction_table = PrettyTable(["Transaction_ID", "Amount", "Type", "Category", "Date", "Note"])
        for i in transaction_list:
            transaction_table.add_row([i["Transaction"]["id"], i["Transaction"]["amount"], i["Transaction"]["type"], i["Transaction"]["category"], i["Transaction"]["date"], i["Transaction"]["note"]])
        print(transaction_table)

        # get expenses data
        expenses_list = []
        expenses_amount = 0
        for a in transaction_list:
            if a["Transaction"]["type"] == "Expense":
                expenses_list.append(a)
                expenses_amount += a["Transaction"]["amount"]

        # get budget data
        try:
            with open("budget_limits.txt", "r") as budget_data:
                budget_file = json.load(budget_data)
            # check budget with total expenses
            check_budget(budget_dict=budget_file, total_expenses=expenses_amount)

            # add all transaction within the same category
            feeding_amount = 0
            airtime_data_amount = 0
            electricity_amount = 0
            betting_amount = 0
            transfer_amount = 0
            for category in expenses_list:
                if category["Transaction"]["category"] == "Feeding":
                    feeding_amount += category["Transaction"]["amount"]

                elif category["Transaction"]["category"] == "Electricity":
                    electricity_amount += category["Transaction"]["amount"]

                elif category["Transaction"]["category"] in ["Airtime" , "Data"]:
                    airtime_data_amount += category["Transaction"]["amount"]

                elif category["Transaction"]["category"] == "Betting":
                    betting_amount += category["Transaction"]["amount"]

                elif category["Transaction"]["category"] == "Transfer":
                    transfer_amount += category["Transaction"]["amount"]
            # check each category total amount and their limits.
            category_total_amount_list = [feeding_amount, airtime_data_amount, electricity_amount, betting_amount, transfer_amount]

            for i, j in zip(category_total_amount_list, list(budget_file.keys())[1:6]):
                check_category_limits(budget_dict=budget_file, category_amount=i, limit=j)
        except FileNotFoundError:
            print("You have not set your Budget or Limits yet")

        new_input = input("Quit Program? y/n ").lower()
        if new_input == "y":
            user_continue = False
            print("Exiting....")

    # if user_input == "Savings"
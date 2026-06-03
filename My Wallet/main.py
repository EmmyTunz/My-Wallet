import pandas as pd
from datetime import datetime

new_transaction = True
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
print(transaction_list)
print(data)


# add transaction to table
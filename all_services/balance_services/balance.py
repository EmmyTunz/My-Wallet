# this file will be used for the balance logic
import json
import os

BASE_URL = os.path.dirname(os.path.abspath(__file__))

class BalanceTracker:
    def __init__(self):
        try:
            with open(os.path.join(BASE_URL, "balance.txt"), "r") as balance_data:
                self.balance = float(balance_data.read())
        except FileNotFoundError:
            self.balance = 0

    def update_balance(self, new_transaction):
        if new_transaction["Transaction"]["type"] == "Income":
            self.balance += new_transaction["Transaction"]["amount"]
            return True

        elif new_transaction["Transaction"]["type"] == "Expense":
            if self.balance < new_transaction["Transaction"]["amount"]:
                return False

            else:
                self.balance -= new_transaction["Transaction"]["amount"]
                return True
        return False


    def save_balance(self):
        with open(os.path.join(BASE_URL, "balance.txt"), "w") as balance_data:
            json.dump(self.balance, balance_data)

    def display_balance(self):
        return self.balance

    # def remove_savings_from_balance(self, log_contribution):
    def remove_savings_from_balance(self, amount):
        self.balance -= amount


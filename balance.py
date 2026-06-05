# this file will be used for the balance logic
import json
class BalanceTracker:
    def __init__(self):
        self.balance = 0

    def update_balance(self, new_transaction):
        if new_transaction["Transaction"]["type"] == "Income":
            self.balance += new_transaction["Transaction"]["amount"]
            return True

        elif new_transaction["Transaction"]["type"] == "Expense":
            if self.balance < new_transaction["Transaction"]["amount"]:
                print("Insufficient Funds! Transaction declined")
                return False

            else:
                self.balance -= new_transaction["Transaction"]["amount"]
                return True
        return False


    def save_balance(self):
        with open("balance.txt", "w") as balance_data:
            json.dump(self.balance, balance_data)

    def display_balance(self):
        print(f"Balance: N{self.balance}")

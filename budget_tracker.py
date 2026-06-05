import json
class BudgetTracker:
    def __init__(self):
        self.feeding_limit = int(input("Enter your monthly feeding budget "))
        self.airtime_data_limit = int(input("Enter your Monthly Airtime/Data limit "))
        self.electricity_limit = int(input("Enter your Monthly electricity limit "))
        self.betting_limit = int(input("Enter your monthly betting limit "))
        self.transfer_limit = int(input("Enter your monthly transfer limit "))
        self.budget = (self.transfer_limit + self.betting_limit + self.feeding_limit + self.electricity_limit +
                       self.airtime_data_limit)


    def save_budget_data(self):
        budget_limit_dict = {
            "budget": self.budget,
            "feeding": self.feeding_limit,
            "airtime/data": self.airtime_data_limit,
            "electricity": self.electricity_limit,
            "betting": self.betting_limit,
            "transfer": self.transfer_limit,
        }
        # save budget data
        with open("budget_limits.txt", "w") as data:
            json.dump(budget_limit_dict, data)



def check_category_limits(limit, category_amount, budget_dict):
    if budget_dict[limit] <= category_amount:
        print(f"You have exceeded your monthly {limit}, you spent a total of N{category_amount}")


def check_budget(budget_dict, total_expenses):
    print(f"Your total budget is N{budget_dict["budget"]}.")
    print(f"You have spent a total of N{total_expenses}.")
    amount_remaining = budget_dict["budget"] - total_expenses
    print(f"You have N{amount_remaining} left to spend.")
    if total_expenses > (80/100) * budget_dict["budget"]:
        print("Warning! You have now spent 80% of your Monthly budget!")
    else:
        pass









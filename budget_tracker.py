class BudgetTracker:
    def __init__(self):
        self.feeding_limit = int(input("Enter your monthly feeding budget "))
        self.airtime_data_limit = int(input("Enter your Monthly Airtime/Data limit "))
        self.electricity_limit = int(input("Enter your Monthly electricity limit "))
        self.betting_limit = int(input("Enter your monthly betting limit "))
        self.transfer_limit = int(input("Enter your monthly transfer limit "))
        self.budget = self.transfer_limit + self.betting_limit + self.feeding_limit + self.electricity_limit + self.airtime_data_limit

    def check_budget(self, total_expenses):
        print(f"Your total budget is N{self.budget}")
        print(f"You have spent a total of N{total_expenses}")
        if total_expenses > (80/100) * self.budget:
            print("Warning! You have now spent 80% of your Monthly budget!")
        else:
            pass









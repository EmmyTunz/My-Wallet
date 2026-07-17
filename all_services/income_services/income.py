from all_services.transactions_services.transaction import load_data


## - calculate the total income in that month
transactions_list = load_data()
def calculate_total_income(transaction_list):
    income_amount = 0
    for a in transaction_list:
        if a["Transaction"]["type"] == "Income":
            income_amount += a["Transaction"]["amount"]
    return income_amount
from all_services.budget_services.budget_tracker import check_category_limits

def expenses_list_func(transaction_list):
    expenses_list = []
    for a in transaction_list:
        if a["Transaction"]["type"] == "Expense":
            expenses_list.append(a)

    return expenses_list

def calculate_categories(expenses_list):
    feeding_amount = 0
    airtime_data_amount = 0
    electricity_amount = 0
    betting_amount = 0
    transfer_amount = 0
    # add all transaction within the same category
    for category in expenses_list:
        if category["Transaction"]["category"] == "Feeding":
            feeding_amount += category["Transaction"]["amount"]

        elif category["Transaction"]["category"] == "Electricity":
            electricity_amount += category["Transaction"]["amount"]

        elif category["Transaction"]["category"] in ["Airtime", "Data"]:
            airtime_data_amount += category["Transaction"]["amount"]

        elif category["Transaction"]["category"] == "Betting":
            betting_amount += category["Transaction"]["amount"]

        elif category["Transaction"]["category"] == "Transfer":
            transfer_amount += category["Transaction"]["amount"]

    category_total_amount_list = [feeding_amount, airtime_data_amount, electricity_amount, betting_amount,
                                  transfer_amount]
    return category_total_amount_list



def check_expenses(expenses_list, budget_file):
    messages = []
    # check each category total amount and their limits.
    category_total_amount_list = calculate_categories(expenses_list)
    for i, j in zip(category_total_amount_list, list(budget_file.keys())[1:6]):
        check = check_category_limits(budget_dict=budget_file, category_amount=i, limit=j)
        messages.append(check)
    return messages



# calculate total expenses
def total_expenses(transaction_list):
    expenses_amount = 0
    for a in transaction_list:
        if a["Transaction"]["type"] == "Expense":
            expenses_amount += a["Transaction"]["amount"]
    return expenses_amount







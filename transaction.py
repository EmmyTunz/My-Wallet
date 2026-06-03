class Transaction:
    def __init__(self):
        self.amount = 0
        self.type = 0
        self.category = 0
        self.date = 0
        self.note = ""

    def save_transaction(self):
        pass

    def del_transaction(self):
        pass



transactions = {"Transaction":{"0":{"amount":10000,"type":"Income","date":1780322240784,"note":"Sweet Sensation"},"1":{"amount":20000,"type":"expenses","date":1780322269518,"note":"wWWss"},"2":{"amount":100000,"type":"Income","date":1780482364566,"note":"thank God"},"3":{"amount":10000,"type":"Expense","date":1780482403690,"note":"Gift data"},"4":{"amount":10000,"type":"Income","date":1780482797304,"note":"May"},"5":{"amount":100000,"type":"expense","date":1780482864701,"note":"benz"},"6":{"amount":2000,"type":"ecpense","date":1780483275806,"note":"eggroll"},"7":{"amount":3000,"type":"expense","date":1780483303549,"note":"gift for sister"}}}

del transactions["Transaction"]["1"]
print(transactions)

# keys = list(transactions["Transaction"].keys())
# print(keys)
# print(keys[len(transactions["Transaction"].keys()) - 1])
class BalanceDisplay:
    def __init__(self):
        self.balance = 1000  # solde initial fictif

    def get_balance(self):
        return self.balance

    def update_balance(self, amount):
        self.balance += amount

class Portfolio:
    def __init__(self):
        self.balance = 1000

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            raise ValueError("Solde insuffisant")

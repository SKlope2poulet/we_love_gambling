class BlackjackGame:
    def __init__(self, balance=1000):
        self.balance = balance
        self.bet = 0

    def start_hand(self, bet):
        self.bet = bet
        self.balance -= bet

class BlackjackGame:
    def __init__(self, balance=1000):
        self.balance = balance
        self.hands = []

    def start_multiple_hands(self, bets):
        self.hands = []
        for bet in bets:
            self.balance -= bet
            self.hands.append({"cards": [], "bet": bet})

class BlackjackGame:
    def __init__(self, balance=1000):
        self.balance = balance
        self.hands = []

    def start_multiple_hands(self, bets):
        self.hands = []
        for bet in bets:
            self.balance -= bet
            self.hands.append({"cards": [], "bet": bet})
    def split(self):
        if len(self.player_hand) == 2 and self.player_hand[0][1] == self.player_hand[1][1]:
            self.hands = [[self.player_hand[0]], [self.player_hand[1]]]

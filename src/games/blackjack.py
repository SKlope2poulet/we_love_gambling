import random

class BlackjackGame:
    def __init__(self, balance=1000):
        self.balance = balance
        self.bet = 0
        self.player_hand = []
        self.deck = [("A", 1), ("2", 2), ("3", 3), ("4", 4)] * 4

    def draw(self):
        return random.choice(self.deck)

    def start_hand(self, bet):
        self.bet = bet
        self.balance -= bet
        self.player_hand = [self.draw(), self.draw()]

    def double(self):
        self.balance -= self.bet
        self.bet *= 2
        self.player_hand.append(self.draw())

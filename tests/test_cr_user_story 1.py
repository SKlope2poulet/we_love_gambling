"""
USER STORY 1 — Choisir la mise
En tant qu’utilisateur, je veux choisir le montant de ma mise afin de tenter un gain.
"""

import tkinter as tk

# === Code à tester ===
class ChickenRoadBet:
    def __init__(self):
        self.balance = 100.0
        self.bet = 0.0
        self.playing = False
        self.bet_entry = None

    def place_bet(self, amount):
        """Valide la mise."""
        try:
            amount = float(amount)
            if amount <= 0 or amount > self.balance:
                raise ValueError
            self.bet = amount
            self.balance -= amount
            self.playing = True
            return True
        except ValueError:
            self.playing = False
            return False


# === Tests ===
def test_place_bet_valid():
    app = ChickenRoadBet()
    assert app.place_bet(10)
    assert app.playing
    assert app.bet == 10
    assert app.balance == 90

def test_place_bet_invalid():
    app = ChickenRoadBet()
    before = app.balance
    assert not app.place_bet(99999)
    assert app.balance == before
    assert not app.playing

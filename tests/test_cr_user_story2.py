"""
USER STORY 2 — Cash-out & perte potentielle
En tant qu’utilisateur, je veux voir une animation lors du cash-out et savoir où j’aurais perdu.
"""

import random

# === Code à tester ===
class ChickenRoadCashOut:
    def __init__(self):
        self.balance = 100.0
        self.bet = 10.0
        self.multipliers = [1.0, 1.5, 2.0, 3.0, 3.5, 4.0]
        self.player_col = 2
        self.playing = True
        self.losing_cell = None

    def _predict_loss_cell(self):
        for c in range(self.player_col + 1, len(self.multipliers)):
            if random.random() < 0.5:
                return c
        return None

    def cash_out(self):
        cur = self.multipliers[self.player_col]
        gain = round(self.bet * cur, 2)
        self.balance += gain
        self.playing = False
        self.losing_cell = self._predict_loss_cell()
        return gain


# === Tests ===
def test_cash_out_adds_gain(monkeypatch):
    app = ChickenRoadCashOut()
    monkeypatch.setattr(app, "_predict_loss_cell", lambda: 4)
    before = app.balance
    gain = app.cash_out()
    assert app.balance == before + gain
    assert not app.playing
    assert app.losing_cell == 4

def test_cash_out_no_loss_possible(monkeypatch):
    app = ChickenRoadCashOut()
    monkeypatch.setattr(app, "_predict_loss_cell", lambda: None)
    app.cash_out()
    assert app.losing_cell is None

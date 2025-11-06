"""
USER STORY 3 — Statistiques et dernier gain
En tant qu’utilisateur, je veux voir un récapitulatif de mon dernier gain ou perte.
"""

# === Code à tester ===
class ChickenRoadStats:
    def __init__(self):
        self.last_win = None
        self.last_lbl = "Dernier gain : —"
        self.difficulty = "Facile"
        self.multipliers = [1.0, 1.5, 2.0, 3.0, 3.5, 4.0]
        self.player_col = 2
        self.bet = 10.0
        self.balance = 100.0
        self.lose = False
        self.playing = True

    def victory(self):
        cur = self.multipliers[self.player_col]
        gain = round(self.bet * cur, 2)
        self.balance += gain
        self.last_win = f"+{gain:.2f}€ (x{cur}) — {self.difficulty}"
        self.last_lbl = f"Dernier gain : {self.last_win}"
        self.playing = False
        return gain

    def defeat(self):
        self.last_lbl = "Dernier gain : PERDU 💀"
        self.playing = False
        self.lose = True
        return self.last_lbl


# === Tests ===
def test_victory_updates_last_win():
    app = ChickenRoadStats()
    gain = app.victory()
    assert "x" in app.last_win
    assert "Dernier gain" in app.last_lbl
    assert app.balance > 100.0
    assert not app.playing

def test_defeat_updates_label():
    app = ChickenRoadStats()
    msg = app.defeat()
    assert "PERDU" in msg
    assert app.lose
    assert not app.playing

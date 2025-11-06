"""
USER STORY 4 — Clic pour avancer
En tant qu’utilisateur, je veux avancer manuellement en cliquant pour décider du risque.
"""

# === Code à tester ===
import random

class ChickenRoadMove:
    def __init__(self):
        self.player_col = 0
        self.cols = 6
        self.playing = True
        self.lose = False

    def _realistic_loss_chance(self): return 0.4

    def advance(self):
        if not self.playing or self.lose:
            return
        self.player_col += 1
        if self.player_col >= self.cols - 2:
            self.playing = False
            return "win"
        if random.random() < self._realistic_loss_chance():
            self.lose = True
            self.playing = False
            return "lose"
        return "continue"


# === Tests ===
def test_advance_increments_player(monkeypatch):
    app = ChickenRoadMove()
    start = app.player_col
    monkeypatch.setattr(app, "_realistic_loss_chance", lambda: 0.0)
    result = app.advance()
    assert result == "continue"
    assert app.player_col == start + 1

def test_advance_triggers_loss(monkeypatch):
    app = ChickenRoadMove()
    monkeypatch.setattr(app, "_realistic_loss_chance", lambda: 1.0)
    result = app.advance()
    assert result == "lose"
    assert app.lose

"""
USER STORY 5 — Animation de défaite
En tant qu’utilisateur, je veux voir une animation visuelle claire lors d’une défaite.
"""

# === Code à tester ===
class ChickenRoadLoss:
    def __init__(self):
        self.lose = False
        self.playing = True
        self.last_lbl = "Dernier gain : —"

    def defeat(self):
        """Change l'état du jeu pour afficher une défaite."""
        self.lose = True
        self.playing = False
        self.last_lbl = "Dernier gain : PERDU 💀"
        return self.last_lbl


# === Tests ===
def test_defeat_state_changes():
    app = ChickenRoadLoss()
    msg = app.defeat()
    assert app.lose
    assert not app.playing
    assert "PERDU" in msg

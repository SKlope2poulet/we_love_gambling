"""
USER STORY 6 — Sélection manuelle de la difficulté
En tant qu’utilisateur, je veux pouvoir choisir entre le mode Facile et le mode Difficile
afin d’adapter le niveau de risque et les multiplicateurs à ma stratégie de jeu.
"""

# === Code à tester ===
class ChickenRoadDifficultyChoice:
    def __init__(self):
        self.difficulty = "Facile"
        self.loss_chance = 0.4  # % de chance de perte par case
        self.multipliers = [1.0, 1.5, 2.0, 3.0, 3.5, 4.0]

    def set_difficulty(self, mode):
        """Change la difficulté du jeu selon le choix de l’utilisateur."""
        if mode not in ["Facile", "Difficile"]:
            raise ValueError("Mode invalide")
        self.difficulty = mode
        if mode == "Facile":
            self.loss_chance = 0.4
            self.multipliers = [1.0, 1.3, 1.7, 2.2, 2.8, 3.3]
        else:  # Difficile
            self.loss_chance = 0.6
            self.multipliers = [1.0, 1.8, 2.5, 3.8, 5.0, 6.5]

    def get_difficulty_info(self):
        """Retourne un résumé textuel du mode actif."""
        return {
            "mode": self.difficulty,
            "chance_perte": self.loss_chance,
            "multipliers": self.multipliers,
        }


# === Tests ===
def test_set_difficulty_to_difficile():
    app = ChickenRoadDifficultyChoice()
    app.set_difficulty("Difficile")
    info = app.get_difficulty_info()
    assert app.difficulty == "Difficile"
    assert info["chance_perte"] == 0.6
    assert info["multipliers"][-1] > 6  # plus élevés qu'en facile

def test_set_difficulty_to_facile():
    app = ChickenRoadDifficultyChoice()
    app.set_difficulty("Facile")
    info = app.get_difficulty_info()
    assert app.difficulty == "Facile"
    assert info["chance_perte"] == 0.4
    assert info["multipliers"][-1] < 4  # plus bas qu'en difficile

def test_invalid_difficulty_raises_error():
    app = ChickenRoadDifficultyChoice()
    try:
        app.set_difficulty("Impossible")
    except ValueError as e:
        assert "invalide" in str(e)
    else:
        assert False, "Erreur attendue non levée"

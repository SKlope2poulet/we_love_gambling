import random


class SlotMachineApp:
    def __init__(self):
        """Initialise la machine à sous avec des valeurs par défaut."""
        self.current_bet = 1               # Mise actuelle de l'utilisateur
        self.reels = ["🍒", "🍋", "⭐"]      # Rouleaux initiaux
        self.reels_history = []            # Historique des combinaisons
        self.total_spins = 0               # Nombre total de tours
        self.total_bet = 0                 # Somme totale misée
        self.total_gain = 0                # Somme totale gagnée

    # --- US1 : Choisir sa mise ---
    def set_bet(self, amount: int):
        """Définit la mise de l'utilisateur."""
        if amount <= 0:
            raise ValueError("La mise doit être positive.")
        self.current_bet = amount

    # --- US2 : Lancer les rouleaux ---
    def spin(self):
        """Fait tourner les rouleaux et calcule un éventuel gain."""
        self.reels = random.choices(["🍒", "🍋", "⭐", "💎", "7️⃣"], k=3)
        self.reels_history.append(tuple(self.reels))
        self.total_spins += 1
        self.total_bet += self.current_bet

        # Règle simple : 3 symboles identiques = gain x5
        if len(set(self.reels)) == 1:
            self.total_gain += self.current_bet * 5

    # --- US3 : Autoplay ---
    def autoplay(self, rounds=10):
        """Lance plusieurs tours automatiquement."""
        for _ in range(rounds):
            self.spin()

    # --- US4 : Récapitulatif session ---
    def get_session_summary(self):
        """Renvoie un récapitulatif des statistiques de session."""
        rtp = (self.total_gain / self.total_bet * 100) if self.total_bet > 0 else 0
        return {
            "total_spins": self.total_spins,
            "total_bet": self.total_bet,
            "total_gain": self.total_gain,
            "rtp": round(rtp, 2)
        }

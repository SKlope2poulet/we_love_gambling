class Dashboard:
    def __init__(self, wins=0, losses=0):
        self.wins = wins
        self.losses = losses

    def win_rate(self):
        total = self.wins + self.losses
        return round((self.wins / total) * 100) if total > 0 else 0

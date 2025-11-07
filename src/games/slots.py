class SlotMachineApp:
    ...
    def __init__(self):
        self.total_spins = 0
        self.reels = ["🍒", "🍋", "⭐"]

    def spin(self):
        import random
        self.reels = random.choices(["🍒", "🍋", "⭐", "💎", "7️⃣"], k=3)
        self.total_spins += 1

    def autoplay(self, rounds=10):
        for _ in range(rounds):
            self.spin()

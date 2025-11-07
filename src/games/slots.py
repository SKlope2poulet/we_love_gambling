import random

class SlotMachineApp:
    def __init__(self):
        self.current_bet = 1
        self.reels = ["🍒", "🍋", "⭐"]

    def set_bet(self, amount):
        self.current_bet = amount

    def spin(self):
        self.reels = random.choices(["🍒", "🍋", "⭐", "💎", "7️⃣"], k=3)

import tkinter as tk

class RechargeButton(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#222222")
        self.parent = parent

        self.button = tk.Button(
            self,
            text="🔄 Recharger le solde fictif",
            bg="#00b894",
            fg="white",
            font=("Arial", 11, "bold"),
            width=25,
            command=self.recharge_balance
        )
        self.button.pack(pady=5)

    def recharge_balance(self):
        """Recharge le solde via le composant Portfolio s'il existe."""
        if hasattr(self.parent, "portfolio"):
            # On recharge en ajoutant 500 € fictifs
            self.parent.portfolio.balance += 500
            self.parent.portfolio.update_main_balance()
        elif hasattr(self.parent, "balance"):
            # Si pas de portfolio (fallback)
            self.parent.balance.update_balance(self.parent.balance.balance + 500)

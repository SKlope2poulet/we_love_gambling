import tkinter as tk

class BalanceDisplay(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#222222")
        self.parent = parent
        self.balance = 1000  # Solde fictif de départ

        self.label_title = tk.Label(
            self,
            text="💰 Solde fictif :",
            bg="#222222",
            fg="white",
            font=("Arial", 12, "bold")
        )
        self.label_title.pack(side="left", padx=5)

        self.label_balance = tk.Label(
            self,
            text=f"{self.balance} €",
            bg="#222222",
            fg="#00ff99",
            font=("Arial", 12, "bold")
        )
        self.label_balance.pack(side="left")

    def update_balance(self, new_balance):
        """Met à jour le solde affiché."""
        self.balance = new_balance
        self.label_balance.config(text=f"{self.balance} €")

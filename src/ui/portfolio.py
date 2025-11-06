import tkinter as tk
from tkinter import messagebox

class Portfolio(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#222222", padx=10, pady=10)
        self.parent = parent
        self.balance = 1000  # solde initial fictif

        tk.Label(
            self,
            text="💼 Gestion du portefeuille",
            bg="#222222",
            fg="white",
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 10))

        btn_frame = tk.Frame(self, bg="#222222")
        btn_frame.pack()

        tk.Button(
            btn_frame,
            text="Déposer +100 €",
            command=self.deposit,
            bg="#007bff",
            fg="white",
            width=15
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="Retirer -100 €",
            command=self.withdraw,
            bg="#ff5555",
            fg="white",
            width=15
        ).pack(side="left", padx=10)

    def deposit(self):
        """Ajoute 100 € au solde et met à jour le composant principal s’il existe."""
        self.balance += 100
        self.update_main_balance()

    def withdraw(self):
        """Retire 100 € du solde si disponible, sinon avertit l’utilisateur."""
        if self.balance >= 100:
            self.balance -= 100
            self.update_main_balance()
        else:
            messagebox.showwarning("Solde insuffisant", "Tu n’as plus assez de fonds fictifs !")

    def update_main_balance(self):
        """Met à jour le solde dans la BalanceDisplay du main si elle existe."""
        if hasattr(self.parent, "balance"):
            self.parent.balance.update_balance(self.balance)

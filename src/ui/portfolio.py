import tkinter as tk

class Portfolio(tk.Frame):
    """Affiche et gère le solde fictif de l'utilisateur."""

    def __init__(self, parent):
        super().__init__(parent, bg="#1e1e1e")
        self.parent = parent
        self.balance = 100.0  # solde initial fictif

        self.label = tk.Label(
            self,
            text=f"💰 Solde actuel : {self.balance:.2f} €",
            fg="white",
            bg="#1e1e1e",
            font=("Arial", 14, "bold"),
        )
        self.label.pack(pady=10)

    def update_display(self):
        """Met à jour l'affichage du solde."""
        self.label.config(text=f"💰 Solde actuel : {self.balance:.2f} €")

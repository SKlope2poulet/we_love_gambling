import tkinter as tk
from tkinter import messagebox

class RechargeButton:
    """Classe logique du bouton 'Recharger le solde'."""

    def __init__(self, parent):
        self.parent = parent
        self.label = "💰 Recharger le solde"  # <-- c’est ce qui manquait

    def recharge(self):
        """Recharge le solde fictif de l'utilisateur."""
        if hasattr(self.parent, "portfolio"):
            # Si un portefeuille existe, on met à jour son solde
            self.parent.portfolio.balance += 100.0
            messagebox.showinfo("Solde rechargé", "💸 +100€ ajoutés à votre solde fictif !")
        else:
            messagebox.showinfo("Information", "Aucun portefeuille détecté.")

import tkinter as tk
from tkinter import messagebox

class LegalPopup(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1e1e1e")
        self.parent = parent

        # Bouton d'accès CGU / politique de confidentialité
        tk.Button(
            self,
            text="📜 CGU & Politique de confidentialité",
            font=("Arial", 11, "bold"),
            bg="#2e2e2e",
            fg="white",
            activebackground="#444444",
            activeforeground="#00ff99",
            relief="flat",
            command=self.show_legal_info,
            width=35
        ).pack(pady=5)

    def show_legal_info(self):
        """Affiche une fenêtre d'information légale."""
        message = (
            "Conditions Générales d’Utilisation :\n"
            "- Ce site est à but ludique et n’implique aucun gain réel.\n"
            "- Aucune donnée personnelle n’est transmise à des tiers.\n"
            "- Les fonds affichés sont purement fictifs.\n\n"
            "Politique de confidentialité :\n"
            "- Vos données sont utilisées uniquement pour simuler des sessions de jeu.\n"
            "- En continuant, vous acceptez ces conditions."
        )
        messagebox.showinfo("Mentions légales", message)

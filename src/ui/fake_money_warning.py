import tkinter as tk
from tkinter import messagebox

class FakeMoneyWarning(tk.Toplevel):
    """Popup avertissant que le site utilise de l'argent fictif."""

    def __init__(self, parent, on_confirm=None):
        super().__init__(parent)
        self.title("⚠️ Avertissement")
        self.geometry("400x250")
        self.configure(bg="#1e1e1e")
        self.on_confirm = on_confirm

        tk.Label(
            self,
            text="💸 ATTENTION : Ce site utilise uniquement de l'argent fictif !\n"
                 "Aucune mise réelle, aucun gain réel.",
            fg="white",
            bg="#1e1e1e",
            wraplength=350,
            justify="center",
            font=("Arial", 12, "bold")
        ).pack(expand=True, pady=20, padx=10)

        tk.Button(
            self,
            text="Je comprends",
            bg="#28a745",
            fg="white",
            command=self.confirm,
            width=20
        ).pack(pady=10)

    def confirm(self):
        """Ferme la fenêtre et passe à l'étape suivante."""
        self.destroy()
        if self.on_confirm:
            self.on_confirm()

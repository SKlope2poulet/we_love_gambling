import tkinter as tk

class FakeMoneyWarning(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1e1e1e", padx=10, pady=10)
        self.parent = parent

        tk.Label(
            self,
            text="⚠️ Argent fictif – aucune mise réelle. Jouez pour le plaisir !",
            fg="#ffcc00",
            bg="#1e1e1e",
            font=("Arial", 11, "bold"),
            wraplength=800,
            justify="center"
        ).pack()

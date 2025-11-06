import tkinter as tk

class Navbar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#333333")
        self.parent = parent
        self.config(height=50)

        # Liens fictifs de navigation
        self.links = ["Accueil", "Jeux", "Tableau de bord", "Portefeuille", "CGU"]

        for link in self.links:
            btn = tk.Button(
                self,
                text=link,
                bg="#333333",
                fg="white",
                font=("Arial", 10, "bold"),
                activebackground="#555555",
                activeforeground="white",
                relief="flat",
                command=lambda l=link: self.navigate(l)
            )
            btn.pack(side="left", padx=15, pady=10)

    def navigate(self, link):
        """Comportement de navigation basique (à adapter plus tard)."""
        print(f"Navigation vers : {link}")

import tkinter as tk

class Dashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1e1e1e", padx=15, pady=15)
        self.parent = parent

        # 🎯 KPI simulés
        self.kpis = {
            "Taux de gain": "68%",
            "Mises totales": "2 450 €",
            "Parties jouées": "128",
            "Dernier gain": "75 €"
        }

        tk.Label(
            self,
            text="📊 Tableau de bord",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#1e1e1e"
        ).pack(anchor="w", pady=(0, 10))

        # Affichage des KPI sous forme de lignes
        for name, value in self.kpis.items():
            frame = tk.Frame(self, bg="#1e1e1e")
            frame.pack(anchor="w", pady=3)

            tk.Label(
                frame, text=f"{name} :", fg="white", bg="#1e1e1e", font=("Arial", 11)
            ).pack(side="left")

            tk.Label(
                frame, text=value, fg="#00ff99", bg="#1e1e1e", font=("Arial", 11, "bold")
            ).pack(side="left", padx=10)

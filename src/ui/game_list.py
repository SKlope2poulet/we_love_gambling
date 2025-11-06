import tkinter as tk

class GameList(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1e1e1e", padx=15, pady=15)
        self.parent = parent

        tk.Label(
            self,
            text="🎮 Liste des jeux disponibles",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#1e1e1e"
        ).pack(anchor="w", pady=(0, 10))

        self.games = [
            "Blackjack ♠️",
            "Slot Machine 🎰",
            "Chicken Road 🐔",
            "Roulette 🎡",
            "Plinko 🟣",
            "Mines Tiles 💣",
            "Penalty Shootout ⚽"
        ]

        # Création des boutons pour chaque jeu
        for game in self.games:
            tk.Button(
                self,
                text=game,
                font=("Arial", 11, "bold"),
                bg="#2e2e2e",
                fg="white",
                activebackground="#444444",
                activeforeground="#00ff99",
                relief="flat",
                width=25,
                command=lambda g=game: self.open_game(g)
            ).pack(pady=4)

    def open_game(self, game_name):
        """Affiche le nom du jeu choisi (pour test)."""
        print(f"Ouverture du jeu : {game_name}")


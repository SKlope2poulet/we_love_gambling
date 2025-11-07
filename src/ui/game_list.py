import tkinter as tk

class GameList(tk.Frame):
    """Liste des jeux disponibles et gestion de l'ouverture des jeux"""

    def __init__(self, parent):
        super().__init__(parent, bg="#1e1e1e")
        self.parent = parent

        # Liste des jeux
        self.games = [
            "Blackjack ♠️",
            "Slot Machine 🎰",
            "Chicken Road 🐔",
            "Roulette 🎡",
            "Plinko 🟣",
            "Mines Tiles 💣",
            "Penalty Shootout ⚽"
        ]

    def open_game(self, game_name):
        """Ouvre le jeu sélectionné"""
        if "plinko" in game_name.lower():
            from src.games.plinko import PlinkoWindow
            PlinkoWindow(self.parent)
        else:
            print(f"Ouverture du jeu : {game_name}")


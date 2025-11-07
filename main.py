import tkinter as tk
from src.games.plinko import PlinkoWindow
from src.games.chicken_road import launch_chicken_road
from src.games.slots import SlotMachineApp
from src.ui.navbar import Navbar
from src.ui.dashboard import Dashboard
from src.ui.portfolio import Portfolio
from src.ui.recharge_button import RechargeButton
from src.ui.game_list import GameList
from src.ui.rules_page import RulesPage
from src.ui.fake_money_warning import FakeMoneyWarning
from src.ui.age_verification import AgeVerification
from src.ui.legal_popup import LegalPopup


def create_homepage():
    """Fonction minimale pour les tests unitaires TDD"""
    return {"navigation": True, "games": []}


class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("We Love Gambling 🎰")
        self.geometry("900x600")
        self.config(bg="#1e1e1e")

        # --- NAVBAR ---
        self.navbar = Navbar(self)
        nav_frame = tk.Frame(self, bg="#2e2e2e", height=40)
        nav_frame.pack(fill="x")
        for link in self.navbar.links:
            tk.Label(
                nav_frame, text=link, fg="white", bg="#2e2e2e", padx=10
            ).pack(side="left")

        # --- DASHBOARD ---
        self.dashboard = Dashboard(self)
        self.dashboard.pack(pady=10)

        # --- PORTFOLIO ---
        self.portfolio = Portfolio(self)
        self.portfolio.pack(pady=10)

        # --- RECHARGE BUTTON ---
        self.recharge_button = RechargeButton(self)
        tk.Button(
            self,
            text=self.recharge_button.label,
            bg="#28a745",
            fg="white",
            width=25,
            command=self.recharge_button.recharge,
        ).pack(pady=10)

        # --- LISTE DES JEUX ---
        self.game_list = GameList(self)
        tk.Label(
            self,
            text="🎮 Liste des jeux disponibles :",
            fg="white",
            bg="#1e1e1e",
            font=("Arial", 14, "bold"),
        ).pack(pady=10)

        for game in self.game_list.games:
            tk.Button(
                self,
                text=game,
                bg="#444",
                fg="white",
                width=20,
                command=lambda g=game: self.open_game(g),
            ).pack(pady=5)

        # --- CGU / Politique de confidentialité ---
        self.legal = LegalPopup(self)
        tk.Button(
            self,
            text="📜 Consulter les CGU / Politique de confidentialité",
            bg="#555",
            fg="white",
            width=40,
            command=self.legal.show_popup,
        ).pack(pady=20)

    # --- MÉTHODES PRINCIPALES ---
    def open_game(self, game_name):
        """Ouvre le jeu choisi."""
        if "plinko" in game_name.lower():
            PlinkoWindow(self, portfolio=self.portfolio)
        elif "slot" in game_name.lower():
            SlotMachineApp(self, portfolio=self.portfolio)
        elif "chicken" in game_name.lower():
            launch_chicken_road(self, portfolio=self.portfolio)
        else:
            self.show_rules(game_name)

    def show_rules(self, game_name):
        """Affiche les règles du jeu."""
        rules = RulesPage(game_name)
        popup = tk.Toplevel(self)
        popup.title(f"Règles du jeu : {game_name}")
        popup.geometry("400x300")
        tk.Label(
            popup,
            text=rules.get_rules(),
            wraplength=350,
            fg="black",
            bg="white",
        ).pack(expand=True, fill="both", padx=20, pady=20)


def launch_app():
    """Démarre l’application avec avertissement et vérification d’âge."""
    root = tk.Tk()
    root.withdraw()  # on cache la fenêtre vide de Tkinter

    # Étape 1 : avertissement argent fictif
    def after_warning():
        # Étape 2 : vérification d’âge
        def after_age_verification():
            # Étape 3 : lancement de la vraie app
            app = HomePage()
            app.mainloop()

        AgeVerification(root, on_confirm=after_age_verification)

    FakeMoneyWarning(root, on_confirm=after_warning)
    root.mainloop()


if __name__ == "__main__":
    launch_app()

import tkinter as tk
from src.ui.navbar import Navbar
from src.ui.balance_display import BalanceDisplay
from src.ui.portfolio import Portfolio
from src.ui.dashboard import Dashboard
from src.ui.fake_money_warning import FakeMoneyWarning
from src.ui.legal_popup import LegalPopup
from src.ui.age_verification import AgeVerification
from src.ui.game_list import GameList
from src.ui.recharge_button import RechargeButton

class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("We Love Gambling 🎰")
        self.geometry("1200x700")
        self.configure(bg="#1a1a1a")

        # ⚠️ Supprime tout double appel ici
        # Afficher la vérification d'âge une seule fois :
        self.has_verified_age = False
        self.after(100, self.show_age_verification)

    def show_age_verification(self):
        if not self.has_verified_age:
            self.has_verified_age = True
            AgeVerification(self, on_confirm=self.launch_app)

    def launch_app(self):
        """Lance la page d'accueil après vérification d'âge."""
        self.clear_window()

        # 🧱 Navbar
        self.navbar = Navbar(self)
        self.navbar.pack(fill="x", pady=5)

        # 🧾 Solde fictif
        self.balance = BalanceDisplay(self)
        self.balance.pack(pady=10)

        # 💳 Portefeuille (dépôt/retrait)
        self.portfolio = Portfolio(self)
        self.portfolio.pack(pady=10)

        # 🔄 Bouton Recharger
        self.recharge = RechargeButton(self)
        self.recharge.pack(pady=10)

        # 📊 Tableau de bord (KPI)
        self.dashboard = Dashboard(self)
        self.dashboard.pack(pady=10)

        # 🎮 Liste des jeux
        self.games = GameList(self)
        self.games.pack(pady=10)

        # ⚖️ CGU / politique confidentialité
        self.legal = LegalPopup(self)

        # 💬 Avertissement "Argent fictif"
        self.fake_money_warning = FakeMoneyWarning(self)
        self.fake_money_warning.pack(pady=5)

    def clear_window(self):
        """Efface tous les widgets pour relancer proprement."""
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = HomePage()
    app.mainloop()

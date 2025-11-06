import tkinter as tk
from tkinter import messagebox
import random, json, os

BANK_FILE = "bank.json"
DEFAULT_BALANCE = 100.0


def load_bank():
    if os.path.exists(BANK_FILE):
        try:
            with open(BANK_FILE, "r") as f:
                return json.load(f).get("balance", DEFAULT_BALANCE)
        except:
            pass
    return DEFAULT_BALANCE


def save_bank(balance):
    with open(BANK_FILE, "w") as f:
        json.dump({"balance": round(balance, 2)}, f)


class Plinko:
    """Logique principale du jeu Plinko (hors interface Tkinter)"""

    def __init__(self, risk="moyen"):
        self.balance = load_bank()
        self.risk = risk
        self.multipliers = {
            "facile": [0.5, 0.8, 1, 1.2, 1.5],
            "moyen": [0.2, 0.5, 1, 2, 4],
            "difficile": [0, 0.3, 1, 3, 8],
        }[risk]

    def play(self, bet):
        """Lancer une bille Plinko et calculer le résultat"""
        if bet <= 0 or bet > self.balance:
            raise ValueError("Mise invalide.")

        slot = random.randint(0, len(self.multipliers) - 1)
        mult = self.multipliers[slot]
        gain = bet * mult

        self.balance = round(self.balance - bet + gain, 2)
        save_bank(self.balance)

        return {"slot": slot, "multiplier": mult, "gain": gain, "balance": self.balance}


class PlinkoWindow(tk.Toplevel):
    """Interface Tkinter du jeu Plinko"""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("🎯 Plinko")
        self.geometry("550x650")
        self.configure(bg="#1e1e1e")

        self.plinko = Plinko("moyen")
        self.create_ui()

    def create_ui(self):
        top = tk.Frame(self, bg="#1e1e1e")
        top.pack(pady=10)

        self.balance_label = tk.Label(
            top, text=f"Solde : {self.plinko.balance:.2f} €", fg="white", bg="#1e1e1e"
        )
        self.balance_label.pack(side="left", padx=10)

        tk.Label(top, text="Mise :", fg="white", bg="#1e1e1e").pack(side="left")
        self.bet_entry = tk.Entry(top, width=5)
        self.bet_entry.insert(0, "5")
        self.bet_entry.pack(side="left", padx=5)

        tk.Label(top, text="Risque :", fg="white", bg="#1e1e1e").pack(side="left")
        self.risk = tk.StringVar(value="moyen")
        tk.OptionMenu(top, self.risk, "facile", "moyen", "difficile").pack(side="left")

        tk.Button(top, text="🎰 Lancer", bg="#00ff99", fg="black", command=self.play).pack(
            side="left", padx=10
        )

    def play(self):
        try:
            bet = float(self.bet_entry.get())
        except:
            messagebox.showerror("Erreur", "Mise invalide.")
            return

        self.plinko.risk = self.risk.get()
        result = self.plinko.play(bet)

        # synchro avec le parent (page d’accueil)
        if hasattr(self.parent, "portfolio"):
            self.parent.portfolio.balance = result["balance"]
            self.parent.portfolio.update_main_balance()

        self.balance_label.config(text=f"Solde : {result['balance']:.2f} €")
        messagebox.showinfo(
            "Résultat", f"Multiplicateur : x{result['multiplier']}\nGain : {result['gain']:.2f} €"
        )

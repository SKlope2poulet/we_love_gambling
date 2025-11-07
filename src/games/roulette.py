import random
import tkinter as tk
from tkinter import ttk, messagebox

# ---------- Modèle (logique) ----------

class Bet:
    """Mise (type, selection, amount)."""
    def __init__(self, type_, selection, amount):
        self.type = str(type_).lower()
        self.selection = selection
        self.amount = float(amount)


class Roulette:
    """Roulette européenne (0-36)."""
    def __init__(self):
        self.pockets = list(range(37))
        self.red_numbers = {
            1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36
        }
        self.columns = {
            1: [n for n in range(1,37) if (n-1)%3==0],
            2: [n for n in range(1,37) if (n-1)%3==1],
            3: [n for n in range(1,37) if (n-1)%3==2],
        }
        self.dozens = {
            1: list(range(1,13)),
            2: list(range(13,25)),
            3: list(range(25,37)),
        }

    def tirer_ROULETTE(self):
        n = random.choice(self.pockets)
        color = 'green' if n == 0 else ('red' if n in self.red_numbers else 'black')
        return n, color

    def gain_pour_mise_ROULETTE(self, bet, outcome_number, outcome_color):
        t, a, n = bet.type, bet.amount, outcome_number
        if t == 'number':
            return 35*a if bet.selection == n else -a
        elif t == 'red':
            return a if outcome_color == 'red' else -a
        elif t == 'black':
            return a if outcome_color == 'black' else -a
        elif t == 'even':
            return a if n != 0 and n % 2 == 0 else -a
        elif t == 'odd':
            return a if n % 2 == 1 else -a
        elif t == 'low':
            return a if 1 <= n <= 18 else -a
        elif t == 'high':
            return a if 19 <= n <= 36 else -a
        elif t == 'dozen':
            d = int(bet.selection)
            return 2*a if n in self.dozens.get(d, []) else -a
        elif t == 'column':
            c = int(bet.selection)
            return 2*a if n in self.columns.get(c, []) else -a
        elif t == 'corner':
            nums = set(bet.selection) if isinstance(bet.selection, (tuple, list, set)) else set()
            return 8*a if n in nums else -a
        else:
            return -a

    def regler_ROULETTE(self, bets):
        n, color = self.tirer_ROULETTE()
        results = []
        net = 0.0
        for b in bets:
            gain = self.gain_pour_mise_ROULETTE(b, n, color)
            results.append((b, gain))
            net += gain
        return n, color, results, net


class Game:
    """Bankroll + liste des mises."""
    def __init__(self, bankroll=500.0):
        self.roulette = Roulette()
        self.bankroll = float(bankroll)
        self.bets = []

    def ajouter_mise(self, bet):
        total_mises = sum(b.amount for b in self.bets)
        if total_mises + bet.amount > self.bankroll:
            return "Mise trop élevée."
        self.bets.append(bet)
        return None

    def lancer(self):
        if not self.bets:
            return "Aucune mise."
        n, color, results, net = self.roulette.regler_ROULETTE(self.bets)
        self.bankroll += net
        self.bets = []
        return n, color, results, net, self.bankroll


# ---------- Interface graphique synchronisée ----------

class RouletteApp(tk.Toplevel):
    """Roulette synchronisée avec le portefeuille principal."""
    def __init__(self, parent, portfolio=None):
        super().__init__(parent)
        self.title("🎡 Roulette Européenne")
        self.geometry("1000x700")
        self.resizable(False, False)

        self.portfolio = portfolio
        bankroll_init = portfolio.balance if portfolio and hasattr(portfolio, "balance") else 500.0
        self.game = Game(bankroll=bankroll_init)

        # Variables UI
        self.click_amount_var = tk.StringVar(value="10")
        self.delete_mode_var = tk.BooleanVar(value=False)
        self.potential_var = tk.StringVar(value="—")

        self._setup_ui()
        self._maj_bankroll()
        self._log("Bienvenue sur la Roulette Européenne !")

    # ---------- Interface ----------
    def _setup_ui(self):
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="💰 Solde :").grid(row=0, column=0, sticky="w")
        self.bankroll_lbl = ttk.Label(top, text="0.00 €")
        self.bankroll_lbl.grid(row=0, column=1, padx=(5, 20))

        ttk.Label(top, text="Mise par clic :").grid(row=0, column=2)
        self.amount_entry = ttk.Entry(top, textvariable=self.click_amount_var, width=8)
        self.amount_entry.grid(row=0, column=3, padx=6)

        ttk.Button(top, text="🎯 Lancer", command=self._lancer_roulette).grid(row=0, column=4, padx=10)
        self.result_label = ttk.Label(top, text="Dernier tirage : —")
        self.result_label.grid(row=0, column=5, padx=10)

        ttk.Label(top, text="Gains potentiels :").grid(row=1, column=0, pady=(8,0))
        self.potential_lbl = ttk.Label(top, textvariable=self.potential_var, wraplength=800, justify="left")
        self.potential_lbl.grid(row=1, column=1, columnspan=6, sticky="w", pady=(8,0))

        # Table placeholder (pour ton Canvas original)
        self.table_frame = ttk.Frame(self)
        self.table_frame.pack(pady=10)
        self.canvas = tk.Canvas(self.table_frame, width=900, height=400, bg="#084f08")
        self.canvas.pack()

        # Historique
        self.history = tk.Text(self, height=10, width=120, state="disabled", bg="#1e1e1e", fg="white")
        self.history.pack(padx=10, pady=(10,20))

    # ---------- Synchronisation ----------
    def _sync_portfolio(self):
        if self.portfolio and hasattr(self.portfolio, "balance"):
            self.portfolio.balance = self.game.bankroll
            if hasattr(self.portfolio, "update_display"):
                self.portfolio.update_display()

    def _maj_bankroll(self):
        self.bankroll_lbl.config(text=f"{self.game.bankroll:.2f} €")
        self._sync_portfolio()

    # ---------- Actions ----------
    def _lancer_roulette(self):
        mise = float(self.click_amount_var.get())
        b = Bet("red", None, mise)  # par défaut une mise rouge, simple démo
        err = self.game.ajouter_mise(b)
        if err:
            messagebox.showwarning("Mise refusée", err)
            return

        res = self.game.lancer()
        if isinstance(res, str):
            messagebox.showinfo("Info", res)
            return

        n, color, results, net, bank = res
        color_fr = {"red": "Rouge", "black": "Noir", "green": "Vert"}[color]
        self.result_label.config(text=f"{n} ({color_fr})")
        self._maj_bankroll()
        self._log(f"Résultat : {n} ({color_fr}) | Gain net : {net:+.2f}€ | Solde : {bank:.2f}€")

    def _log(self, txt):
        self.history.config(state="normal")
        self.history.insert("end", txt + "\n")
        self.history.see("end")
        self.history.config(state="disabled")


# ---------- Helper ----------
def launch_roulette(parent, portfolio):
    """Ouvre la roulette synchronisée."""
    RouletteApp(parent, portfolio=portfolio)


# ---------- MAIN ----------
if __name__ == "__main__":
    root = tk.Tk()
    RouletteApp(root)
    root.mainloop()

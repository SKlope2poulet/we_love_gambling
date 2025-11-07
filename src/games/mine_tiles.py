import tkinter as tk
import random
import math

# ---------- CONFIG ----------
ROWS = 5
COLS = 5
BG = "#1a1b26"
COVER = "#3b4261"
REVEALED = "#24283b"
BOMB_COLOR = "#f7768e"
GEM_COLOR = "#9ece6a"
TEXT_COLOR = "#c0caf5"
BTN_FONT = ("Consolas", 14, "bold")
# -----------------------------


class Cell:
    def __init__(self):
        self.has_bomb = False
        self.revealed = False


class MineTilesGame:
    def __init__(self, bombs):
        self.rows = ROWS
        self.cols = COLS
        self.bombs = bombs
        self.grid = [[Cell() for _ in range(COLS)] for _ in range(ROWS)]
        self._place_bombs()
        self.revealed_count = 0
        self.status = "playing"

    def _place_bombs(self):
        all_cells = [(r, c) for r in range(ROWS) for c in range(COLS)]
        for (r, c) in random.sample(all_cells, self.bombs):
            self.grid[r][c].has_bomb = True

    def reveal(self, r, c):
        cell = self.grid[r][c]
        if cell.revealed or self.status != "playing":
            return
        cell.revealed = True
        if cell.has_bomb:
            self.status = "lost"
            return False
        else:
            self.revealed_count += 1
            return True


class MineTilesApp(tk.Toplevel):
    """Fenêtre MineTiles synchronisée avec le portefeuille principal."""
    def __init__(self, parent, portfolio=None):
        super().__init__(parent)
        self.title("💎 MineTiles Cash")
        self.configure(bg=BG)
        self.portfolio = portfolio
        self.wallet = (portfolio.balance if portfolio and hasattr(portfolio, "balance") else 100)
        self.bet = 10
        self.bombs = 5
        self.multiplier = 1.0
        self.game = MineTilesGame(self.bombs)
        self._setup_ui()
        self._update_labels()

    # ---------- UI ----------
    def _setup_ui(self):
        self.header = tk.Label(self, text="", bg=BG, fg=TEXT_COLOR, font=("Consolas", 14))
        self.header.pack(pady=5)

        self.info = tk.Label(self, text="", bg=BG, fg=TEXT_COLOR, font=("Consolas", 12))
        self.info.pack()

        self.board = tk.Frame(self, bg=BG)
        self.board.pack(pady=10)
        self.buttons = []
        for r in range(ROWS):
            row = []
            for c in range(COLS):
                b = tk.Button(self.board, text="", width=5, height=2, bg=COVER, fg=TEXT_COLOR,
                              font=BTN_FONT, command=lambda rr=r, cc=c: self.click(rr, cc))
                b.grid(row=r, column=c, padx=3, pady=3)
                row.append(b)
            self.buttons.append(row)

        controls = tk.Frame(self, bg=BG)
        controls.pack(pady=5)

        # --- Ajustement de la mise avec + et - ---
        bet_frame = tk.Frame(controls, bg=BG)
        bet_frame.grid(row=0, column=0, columnspan=4, pady=4)

        tk.Label(bet_frame, text="💰 Mise :", bg=BG, fg=TEXT_COLOR, font=BTN_FONT).grid(row=0, column=0, padx=5)

        self.bet_label = tk.Label(bet_frame, text=f"{self.bet}", bg=BG, fg=TEXT_COLOR, font=BTN_FONT, width=5)
        self.bet_label.grid(row=0, column=1, padx=5)

        tk.Button(bet_frame, text=" - ", font=BTN_FONT, command=self.dec_bet).grid(row=0, column=2, padx=2)
        tk.Button(bet_frame, text=" + ", font=BTN_FONT, command=self.inc_bet).grid(row=0, column=3, padx=2)

        # Nombre de bombes
        self.bomb_label = tk.Label(controls, text=f"💣 Bombes : {self.bombs}", bg=BG, fg=TEXT_COLOR, font=BTN_FONT)
        self.bomb_label.grid(row=1, column=0, columnspan=2, pady=5)
        tk.Button(controls, text=" - ", command=self.dec_bombs, font=BTN_FONT).grid(row=1, column=2, padx=2)
        tk.Button(controls, text=" + ", command=self.inc_bombs, font=BTN_FONT).grid(row=1, column=3, padx=2)

        self.cashout_btn = tk.Button(self, text="💰 CASH OUT", command=self.cashout, font=BTN_FONT, bg="#9ece6a")
        self.cashout_btn.pack(pady=5)
        self.restart_btn = tk.Button(self, text="🔄 Nouvelle partie", command=self.restart, font=BTN_FONT, bg="#7aa2f7")
        self.restart_btn.pack(pady=5)

    # ---------- SYNCHRO ----------
    def sync_portfolio(self):
        """Met à jour le portefeuille global."""
        if self.portfolio and hasattr(self.portfolio, "balance"):
            self.portfolio.balance = self.wallet
            if hasattr(self.portfolio, "update_display"):
                self.portfolio.update_display()

    # ---------- LOGIQUE ----------
    def inc_bet(self):
        """Augmente la mise de 1 sans dépasser le solde."""
        if self.bet < self.wallet:
            self.bet += 1
            self._update_labels()

    def dec_bet(self):
        """Diminue la mise de 1 sans descendre sous 1."""
        if self.bet > 1:
            self.bet -= 1
            self._update_labels()

    def click(self, r, c):
        g = self.game
        if g.status != "playing":
            return
        res = g.reveal(r, c)
        self._update_board()
        if res is False:
            self._lose()
        elif res is True:
            self.multiplier = self._calc_multiplier()
            self._update_labels()

    def _lose(self):
        self.wallet -= self.bet
        if self.wallet < 0:
            self.wallet = 0
        self.sync_portfolio()
        self._reveal_all()
        self.header.config(text="💥 BOUM ! Tu as perdu ta mise.", fg=BOMB_COLOR)
        self.info.config(text=f"Solde : {self.wallet} | Multiplier final : x{self.multiplier:.2f}")

    def cashout(self):
        g = self.game
        if g.status != "playing":
            return
        gain = round(self.bet * self.multiplier, 2)
        self.wallet += gain
        self.sync_portfolio()
        g.status = "cashout"
        self._reveal_all()
        self.header.config(text=f"💰 Tu encaisses {gain} crédits !", fg=GEM_COLOR)
        self.info.config(text=f"Nouveau solde : {self.wallet}")

    def restart(self):
        if self.wallet <= 0:
            self.header.config(text="Solde insuffisant.", fg=BOMB_COLOR)
            return
        self.multiplier = 1.0
        self.game = MineTilesGame(self.bombs)
        self._update_board()
        self._update_labels()
        self.header.config(text="", fg=TEXT_COLOR)

    # ---------- BOMBES ----------
    def inc_bombs(self):
        if self.bombs < 20:
            self.bombs += 1
            self.new_game_on_bomb_change()

    def dec_bombs(self):
        if self.bombs > 1:
            self.bombs -= 1
            self.new_game_on_bomb_change()

    def new_game_on_bomb_change(self):
        self.multiplier = 1.0
        self.game = MineTilesGame(self.bombs)
        self._update_board()
        self._update_labels()
        self.header.config(text=f"💣 Nouvelle partie avec {self.bombs} bombes !", fg="#7aa2f7")

    # ---------- AFFICHAGE ----------
    def _update_board(self):
        g = self.game
        for r in range(ROWS):
            for c in range(COLS):
                cell = g.grid[r][c]
                b = self.buttons[r][c]
                if cell.revealed:
                    if cell.has_bomb:
                        b.config(bg=BOMB_COLOR, text="💣", state="disabled")
                    else:
                        b.config(bg=GEM_COLOR, text="💎", state="disabled")
                else:
                    b.config(bg=COVER, text="", state="normal")

    def _reveal_all(self):
        g = self.game
        for r in range(ROWS):
            for c in range(COLS):
                cell = g.grid[r][c]
                b = self.buttons[r][c]
                if cell.has_bomb:
                    b.config(bg=BOMB_COLOR, text="💣", state="disabled")
                elif cell.revealed:
                    b.config(bg=GEM_COLOR, text="💎", state="disabled")
                else:
                    b.config(bg=COVER, text="", state="disabled")

    def _calc_multiplier(self):
        total = ROWS * COLS
        bombs = self.bombs
        revealed = self.game.revealed_count
        prob = 1.0
        safe = total - bombs
        for i in range(revealed):
            prob *= (safe - i) / (total - i)
        if prob == 0:
            prob = 0.0001
        base_mult = (1 / prob) ** 0.25
        risk_bonus = 1 + (bombs / total) * 2.0
        mult = base_mult * risk_bonus
        return round(mult, 2)

    def _update_labels(self):
        self.bomb_label.config(text=f"💣 Bombes : {self.bombs}")
        self.info.config(text=f"Solde : {self.wallet} | Mise : {self.bet} | x{self.multiplier:.2f}")
        if hasattr(self, "bet_label"):
            self.bet_label.config(text=f"{self.bet}")
        self.sync_portfolio()


# ---------- Helper pour intégration ----------
def launch_mine_tiles(parent, portfolio):
    """Ouvre le jeu MineTiles dans une fenêtre enfant synchronisée."""
    MineTilesApp(parent, portfolio=portfolio)


# ---------- MAIN (local) ----------
if __name__ == "__main__":
    app = MineTilesApp(None)
    app.mainloop()

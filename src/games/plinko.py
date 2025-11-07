import tkinter as tk
from tkinter import messagebox
import random, json, os, time, threading, math

BANK_FILE = "bank.json"
DEFAULT_BALANCE = 100.0

CONFIG = {
    "rows": 12,
    "multipliers": [12, 5, 3, 2, 1, 0.6, 0.3, 0.6, 1, 2, 3, 5, 12]
}


def load_bank():
    if os.path.exists(BANK_FILE):
        try:
            with open(BANK_FILE, "r") as f:
                data = json.load(f)
                return data.get("balance", DEFAULT_BALANCE)
        except:
            pass
    return DEFAULT_BALANCE


def save_bank(balance):
    with open(BANK_FILE, "w") as f:
        json.dump({"balance": round(balance, 2)}, f)


class PlinkoWindow(tk.Toplevel):
    """Fenêtre de jeu Plinko synchronisée avec le solde principal."""

    def __init__(self, parent, portfolio=None):
        super().__init__(parent)
        self.title("🎰 Plinko - Mode Difficile équilibré")
        self.geometry("600x700")

        self.parent = parent
        self.portfolio = portfolio
        self.balance = portfolio.balance if portfolio else load_bank()
        self.active_balls = []

        self.setup_ui()
        self.draw_board()

    def setup_ui(self):
        top = tk.Frame(self)
        top.pack(pady=5)
        self.balance_label = tk.Label(top, text=f"Solde : {self.balance:.2f} €", font=("Arial", 12, "bold"))
        self.balance_label.pack(side="left", padx=10)

        tk.Button(top, text="💰 Déposer", command=self.deposit).pack(side="left", padx=5)
        tk.Button(top, text="💸 Retirer", command=self.withdraw).pack(side="left", padx=5)

        self.canvas = tk.Canvas(self, width=500, height=500, bg="black")
        self.canvas.pack(pady=10)

        control = tk.Frame(self)
        control.pack()

        tk.Label(control, text="Mise (€):").grid(row=0, column=0)
        self.bet_entry = tk.Entry(control, width=5)
        self.bet_entry.insert(0, "5")
        self.bet_entry.grid(row=0, column=1)

        tk.Button(control, text="🎯 Lancer", command=self.start_game).grid(row=0, column=2, padx=5)

        self.history = tk.Text(self, height=8, width=60, bg="#111", fg="lime", state="disabled")
        self.history.pack(pady=10)

    def draw_board(self):
        self.canvas.delete("all")
        rows = CONFIG["rows"]
        width, height = 500, 450
        spacing_x = width / (rows + 1)
        spacing_y = height / (rows + 2)

        self.pegs = []
        peg_radius = 5
        for r in range(rows):
            row_pegs = []
            for c in range(r + 1):
                x = (c + 0.5) * spacing_x + (rows - r) * spacing_x / 2
                y = (r + 1) * spacing_y
                self.canvas.create_oval(x - peg_radius, y - peg_radius, x + peg_radius, y + peg_radius, fill="white", outline="")
                row_pegs.append((x, y))
            self.pegs.append(row_pegs)

        # cases des multiplicateurs
        mults = CONFIG["multipliers"]
        self.slots = []
        base_y = (rows + 1) * spacing_y + 10
        slot_width = width / len(mults)
        for i, m in enumerate(mults):
            x0 = i * slot_width
            x1 = (i + 1) * slot_width
            y0 = base_y - 30
            y1 = base_y + 30
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="gray", width=1)
            self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=f"x{m:g}", fill="yellow", font=("Arial", 11, "bold"))
            self.slots.append((x0, x1, m, y0, y1))

        self.rows = rows
        self.spacing_x = spacing_x
        self.spacing_y = spacing_y

    def start_game(self):
        try:
            bet = float(self.bet_entry.get())
            if bet <= 0:
                raise ValueError
        except:
            messagebox.showerror("Erreur", "Mise invalide.")
            return

        if bet > self.balance:
            messagebox.showwarning("Solde insuffisant", "Tu n’as pas assez d’argent.")
            return

        self.balance -= bet
        self.update_balance()
        threading.Thread(target=self.play_once, args=(bet,), daemon=True).start()

    def play_once(self, bet):
        slot_index = self.animate_ball()
        mult = CONFIG["multipliers"][slot_index]
        gain = bet * mult
        self.balance += gain
        self.update_balance()
        self.log(f"Bille → slot {slot_index} | x{mult:.2f} | gain {gain:.2f} €")

    def animate_ball(self):
        x, y = 250, 20
        vx, vy = 0, 0
        gravity = 0.5
        radius = 8
        damping = 0.7
        ball = self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="red")
        self.active_balls.append(ball)

        while True:
            vy += gravity
            x += vx
            y += vy

            for row in self.pegs:
                for peg_x, peg_y in row:
                    dx, dy = x - peg_x, y - peg_y
                    dist = math.hypot(dx, dy)
                    if dist < 10:
                        angle = math.atan2(dy, dx)
                        speed = math.hypot(vx, vy) * damping
                        vx = math.cos(angle) * speed + (random.random() - 0.5) * 0.3
                        vy = -abs(math.sin(angle) * speed)
                        y += 2

            self.canvas.coords(ball, x - radius, y - radius, x + radius, y + radius)
            self.canvas.update()
            time.sleep(0.025)

            for i, (x0, x1, m, y0, y1) in enumerate(self.slots):
                if x0 <= x <= x1 and y >= y0:
                    self.canvas.itemconfig(ball, fill="green")
                    self.canvas.update()
                    threading.Thread(target=self.delete_ball_after_delay, args=(ball,), daemon=True).start()
                    time.sleep(0.5)
                    return i

    def delete_ball_after_delay(self, ball):
        time.sleep(3)
        if ball in self.active_balls:
            self.canvas.delete(ball)
            self.active_balls.remove(ball)

    def update_balance(self):
        self.balance_label.config(text=f"Solde : {self.balance:.2f} €")
        save_bank(self.balance)
        if self.portfolio:
            self.portfolio.balance = self.balance
            self.portfolio.update_display()

    def deposit(self):
        amt = self.ask_amount("Déposer des fonds (€)")
        if amt > 0:
            self.balance += amt
            self.update_balance()

    def withdraw(self):
        amt = self.ask_amount("Retirer des fonds (€)")
        if amt > 0 and amt <= self.balance:
            self.balance -= amt
            self.update_balance()
        else:
            messagebox.showwarning("Erreur", "Montant invalide ou supérieur au solde.")

    def ask_amount(self, title):
        win = tk.Toplevel(self)
        win.title(title)
        tk.Label(win, text=title).pack(padx=10, pady=5)
        entry = tk.Entry(win)
        entry.pack(padx=10, pady=5)
        val = tk.DoubleVar(value=0)
        def ok():
            try:
                val.set(float(entry.get()))
            except:
                val.set(0)
            win.destroy()
        tk.Button(win, text="OK", command=ok).pack(pady=5)
        win.wait_window()
        return val.get()

    def log(self, text):
        self.history.config(state="normal")
        self.history.insert("end", text + "\n")
        self.history.see("end")
        self.history.config(state="disabled")

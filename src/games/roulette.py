import tkinter as tk
from tkinter import messagebox
import random
import math
import threading
import time

class RouletteApp(tk.Toplevel):
    """Jeu de roulette connecté au portefeuille principal."""

    def __init__(self, parent=None, portfolio=None):
        super().__init__(parent)
        self.title("🎡 Roulette - We Love Gambling")
        self.geometry("800x600")
        self.configure(bg="#1e1e1e")

        self.parent = parent
        self.portfolio = portfolio
        self.balance = portfolio.balance if portfolio else 100.0

        # État de jeu
        self.current_bet = 0
        self.bet_choice = None
        self.result_number = None
        self.spin_running = False

        self.create_widgets()
        self.update_balance_label()

    # ------------------ UI ------------------
    def create_widgets(self):
        tk.Label(self, text="🎡 Roulette", font=("Arial", 20, "bold"), fg="white", bg="#1e1e1e").pack(pady=10)

        self.balance_label = tk.Label(self, text="", fg="lime", bg="#1e1e1e", font=("Arial", 14, "bold"))
        self.balance_label.pack(pady=5)

        bet_frame = tk.Frame(self, bg="#1e1e1e")
        bet_frame.pack(pady=10)

        tk.Label(bet_frame, text="💵 Mise (€) :", fg="white", bg="#1e1e1e").grid(row=0, column=0, padx=5)
        self.bet_entry = tk.Entry(bet_frame, width=8)
        self.bet_entry.insert(0, "5")
        self.bet_entry.grid(row=0, column=1, padx=5)

        # Boutons de choix (pair/impair)
        tk.Label(self, text="🎯 Choisissez votre pari :", fg="white", bg="#1e1e1e").pack(pady=5)
        choice_frame = tk.Frame(self, bg="#1e1e1e")
        choice_frame.pack()

        tk.Button(choice_frame, text="🔴 Pair", bg="red", fg="white", width=10, command=lambda: self.set_choice("pair")).grid(row=0, column=0, padx=5)
        tk.Button(choice_frame, text="⚫ Impair", bg="black", fg="white", width=10, command=lambda: self.set_choice("impair")).grid(row=0, column=1, padx=5)
        tk.Button(choice_frame, text="🟢 0 (Jackpot)", bg="green", fg="white", width=10, command=lambda: self.set_choice("zero")).grid(row=0, column=2, padx=5)

        tk.Button(self, text="🎰 Lancer la roue", bg="#28a745", fg="white", width=20, command=self.start_spin).pack(pady=10)

        # Canvas pour dessiner la roue
        self.canvas = tk.Canvas(self, width=400, height=400, bg="#111")
        self.canvas.pack(pady=10)
        self.draw_wheel()

        # Zone d’historique
        self.history = tk.Text(self, height=8, width=70, bg="#222", fg="white", state="disabled")
        self.history.pack(pady=10)

    # ------------------ Logique ------------------
    def set_choice(self, choice):
        self.bet_choice = choice
        self.log(f"🎯 Pari sélectionné : {choice}")

    def start_spin(self):
        if self.spin_running:
            return

        try:
            bet = float(self.bet_entry.get())
            if bet <= 0:
                raise ValueError
        except:
            messagebox.showerror("Erreur", "Veuillez entrer une mise valide.")
            return

        if bet > self.balance:
            messagebox.showwarning("Solde insuffisant", "Vous n’avez pas assez d’argent.")
            return

        if not self.bet_choice:
            messagebox.showinfo("Aucun pari", "Choisissez Pair, Impair ou 0 avant de jouer.")
            return

        # Déduction de la mise
        self.balance -= bet
        self.update_balance_label()

        self.current_bet = bet
        self.spin_running = True
        threading.Thread(target=self.animate_spin, daemon=True).start()

    def animate_spin(self):
        self.log("🎡 La roue tourne...")
        self.canvas.delete("indicator")
        steps = 30
        for i in range(steps):
            self.canvas.itemconfig("wheel", start=random.randint(0, 360))
            self.canvas.update()
            time.sleep(0.05 + i * 0.01)

        # Résultat final
        result = random.randint(0, 36)
        color = "green" if result == 0 else ("red" if result % 2 == 0 else "black")
        self.result_number = result

        # Affiche le numéro gagnant
        self.canvas.create_text(200, 200, text=str(result), font=("Arial", 40, "bold"), fill=color, tags="indicator")

        # Vérifie si le joueur a gagné
        self.check_result(result)

        self.spin_running = False

    def check_result(self, result):
        """Calcule le gain selon le pari"""
        gain = 0
        if self.bet_choice == "zero" and result == 0:
            gain = self.current_bet * 10
            self.log(f"💸 Jackpot ! Vous gagnez {gain:.2f} € avec le 0 !")
        elif self.bet_choice == "pair" and result != 0 and result % 2 == 0:
            gain = self.current_bet * 2
            self.log(f"✅ Résultat {result} (pair) → gain {gain:.2f} €")
        elif self.bet_choice == "impair" and result % 2 != 0:
            gain = self.current_bet * 2
            self.log(f"✅ Résultat {result} (impair) → gain {gain:.2f} €")
        else:
            self.log(f"❌ Résultat {result} → vous perdez votre mise ({self.current_bet:.2f} €)")

        # Mise à jour du solde
        self.balance += gain
        self.update_balance_label()

    def update_balance_label(self):
        self.balance_label.config(text=f"💰 Solde : {self.balance:.2f} €")
        if self.portfolio:
            self.portfolio.balance = self.balance
            if hasattr(self.portfolio, "update_display"):
                self.portfolio.update_display()

    def draw_wheel(self):
        """Dessine la roue de la roulette"""
        colors = ["red", "black"] * 18 + ["green"]
        angle_step = 360 / 37
        for i, color in enumerate(colors):
            start = i * angle_step
            self.canvas.create_arc(50, 50, 350, 350, start=start, extent=angle_step, fill=color, outline="white", tags="wheel")

    def log(self, message):
        """Ajoute un message à l’historique"""
        self.history.config(state="normal")
        self.history.insert("end", message + "\n")
        self.history.see("end")
        self.history.config(state="disabled")

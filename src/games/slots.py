import tkinter as tk
import random
from tkinter import messagebox


class SlotMachineApp(tk.Toplevel):
    def __init__(self, parent, portfolio):
        super().__init__(parent)
        self.title("🎰 Slot Machine")
        self.geometry("500x560")
        self.config(bg="#121212")
        self.resizable(False, False)

        # === Données principales ===
        self.portfolio = portfolio
        self.balance = self.portfolio.balance
        self.current_bet = 10
        self.symbols = ["🍒", "🍋", "⭐", "💎", "7️"]
        self.is_spinning = False
        self.auto_mode = False
        self.auto_spins_remaining = 0

        # === Interface ===
        tk.Label(
            self,
            text="🎰 SLOT MACHINE 🎰",
            font=("Arial", 18, "bold"),
            fg="#FFD700",
            bg="#121212"
        ).pack(pady=20)

        # Solde
        self.balance_label = tk.Label(
            self,
            text=f"Solde : {self.balance:.2f} €",
            font=("Arial", 14),
            fg="#00FF88",
            bg="#121212"
        )
        self.balance_label.pack(pady=5)

        # Zone des rouleaux
        self.reel_frame = tk.Frame(self, bg="#1f1f1f", relief="ridge", bd=5)
        self.reel_frame.pack(pady=30)

        self.reels = [
            tk.Label(
                self.reel_frame,
                text="❔",
                font=("Arial", 40),
                width=3,
                bg="#1f1f1f",
                fg="#FFD700"
            ) for _ in range(3)
        ]
        for r in self.reels:
            r.pack(side="left", padx=20)

        # Mise
        self.bet_label = tk.Label(
            self,
            text=f"Mise actuelle : {self.current_bet} €",
            fg="#FFFFFF",
            bg="#121212",
            font=("Arial", 12)
        )
        self.bet_label.pack(pady=5)

        bet_controls = tk.Frame(self, bg="#121212")
        bet_controls.pack(pady=5)
        tk.Button(
            bet_controls, text="−", command=self.decrease_bet,
            bg="#333", fg="white", width=5
        ).pack(side="left", padx=10)
        tk.Button(
            bet_controls, text="+", command=self.increase_bet,
            bg="#333", fg="white", width=5
        ).pack(side="left", padx=10)

        # Boutons de jeu
        control_frame = tk.Frame(self, bg="#121212")
        control_frame.pack(pady=20)
        tk.Button(
            control_frame,
            text="🎰 SPIN 🎰",
            command=self.start_spin,
            bg="#00A86B",
            fg="white",
            font=("Arial", 14, "bold"),
            width=13,
            height=2
        ).pack(side="left", padx=10)
        tk.Button(
            control_frame,
            text="🔁 AUTOSPIN (10 tours)",
            command=lambda: self.start_autospin(10),
            bg="#5555FF",
            fg="white",
            font=("Arial", 12, "bold"),
            width=17,
            height=2
        ).pack(side="left", padx=10)

        # Résultat
        self.result_label = tk.Label(
            self,
            text="Bonne chance 🍀",
            font=("Arial", 12, "bold"),
            fg="#FFD700",
            bg="#121212"
        )
        self.result_label.pack(pady=10)

    # === Gestion du solde ===
    def update_balance(self):
        """Met à jour la balance dans le jeu et l'interface principale."""
        self.portfolio.balance = self.balance
        self.portfolio.update_display()
        self.balance_label.config(text=f"Solde : {self.balance:.2f} €")

    def increase_bet(self):
        self.current_bet += 5
        self.bet_label.config(text=f"Mise actuelle : {self.current_bet} €")

    def decrease_bet(self):
        if self.current_bet > 5:
            self.current_bet -= 5
            self.bet_label.config(text=f"Mise actuelle : {self.current_bet} €")

    # === Spin manuel ===
    def start_spin(self):
        """Lance un spin manuel."""
        if self.is_spinning or self.auto_mode:
            return
        self._launch_spin()

    # === Autospin ===
    def start_autospin(self, rounds=10):
        """Lance plusieurs spins automatiques."""
        if self.is_spinning or self.auto_mode:
            return
        if self.balance < self.current_bet:
            messagebox.showwarning("Solde insuffisant", "💸 Vous n'avez pas assez de solde pour lancer un autospin !")
            return
        self.auto_mode = True
        self.auto_spins_remaining = rounds
        self._launch_spin()

    def _launch_spin(self):
        """Commence un spin avec animation."""
        if self.balance < self.current_bet:
            messagebox.showwarning("Solde insuffisant", "💸 Vous n'avez pas assez de solde pour jouer !")
            self.auto_mode = False
            return

        self.is_spinning = True
        self.balance -= self.current_bet
        self.update_balance()
        self.result_label.config(text="🎲 Les rouleaux tournent...", fg="#FFD700")

        self.animation_frames = 15
        self.animate_reels()

    def animate_reels(self):
        """Animation des rouleaux."""
        for r in self.reels:
            r.config(text=random.choice(self.symbols))

        self.animation_frames -= 1
        if self.animation_frames > 0:
            self.after(50, self.animate_reels)
        else:
            self.show_result()

    def show_result(self):
        """Affiche le résultat du spin et gère le gain."""
        # 🎲 plus de chance de gagner : 1 chance sur 3 (contre 1/5 classique)
        chance = random.random()
        if chance < 0.33:
            symbols = [random.choice(["🍒", "💎", "7️⃣"])] * 3  # Jackpot plus fréquent
        else:
            symbols = random.choices(self.symbols, k=3)

        for i, s in enumerate(symbols):
            self.reels[i].config(text=s)

        if len(set(symbols)) == 1:
            gain = self.current_bet * 5
            self.balance += gain
            self.result_label.config(text=f"🎉 JACKPOT ! +{gain:.2f} €", fg="#00FF88")
        else:
            self.result_label.config(text="😢 Perdu, retente ta chance", fg="#FF5555")

        self.update_balance()
        self.is_spinning = False

        # Si autospin actif → relancer un spin automatiquement
        if self.auto_mode:
            self.auto_spins_remaining -= 1
            if self.auto_spins_remaining > 0:
                self.after(800, self._launch_spin)
            else:
                self.auto_mode = False
                self.result_label.config(text="🔁 Autospin terminé !", fg="#FFD700")

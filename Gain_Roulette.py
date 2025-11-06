import random
import tkinter as tk
from tkinter import ttk, messagebox

# ---------- Modèle (logique) ----------

class Bet:
    """Mise (type, selection, amount). selection: int/None/tuple(int,int,int,int) pour 'corner'."""
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
            1: [n for n in range(1,37) if (n-1)%3==0],  # bas
            2: [n for n in range(1,37) if (n-1)%3==1],  # milieu
            3: [n for n in range(1,37) if (n-1)%3==2],  # haut
        }
        self.dozens = {
            1: list(range(1,13)),
            2: list(range(13,25)),
            3: list(range(25,37)),
        }

class Game:
    """Bankroll + liste des mises (fusion par (type, selection))."""
    def __init__(self, bankroll=500.0):
        self.roulette = Roulette()
        self.bankroll = float(bankroll)
        self.bets = []

def _libelle_zone_ROULETTE(self, typ, sel):
    if typ == "number": return f"Plein {sel}"
    if typ == "corner": return "Carré " + "-".join(str(x) for x in sel)
    if typ == "dozen":  return {1:"1re 12",2:"2e 12",3:"3e 12"}.get(sel,"Douzaine")
    if typ == "column": return f"Colonne {sel}"
    if typ == "red": return "Rouge"
    if typ == "black": return "Noir"
    if typ == "even": return "PAIR"
    if typ == "odd":  return "IMPAIR"
    if typ == "low":  return "1-18"
    if typ == "high": return "19-36"
    return typ

def _multiplicateur_net_ROULETTE(self, typ):
    # multiplicateur de PROFIT NET (pas retour total)
    return {
        "number": 35,
        "red": 1, "black": 1, "even": 1, "odd": 1, "low": 1, "high": 1,
        "dozen": 2, "column": 2,
        "corner": 8
    }.get(typ, 0)

def _couleur_pour_numero_ROULETTE(self, n):
    rs = self.game.roulette.red_numbers
    return "green" if n == 0 else ("red" if n in rs else "black")

def maj_gains_potentiels_ROULETTE(self):
    """Met à jour le texte 'Gains potentiels' : par mise + meilleur/pire cas."""
    if not self.game.bets:
        self.potential_var.set("—")
        return

    # agrégation par (type, selection)
    agg = {}
    for b in self.game.bets:
        ksel = b.selection if b.type != 'corner' else tuple(sorted(b.selection))
        k = (b.type, ksel)
        agg[k] = agg.get(k, 0.0) + b.amount

    # par mise
    parts, total_stake = [], 0.0
    for (typ, sel), amt in agg.items():
        total_stake += amt
        net = self._multiplicateur_net_ROULETTE(typ) * amt
        parts.append(f"{self._libelle_zone_ROULETTE(typ, sel)}: +{net:.2f}€")

    # meilleur/pire cas sur 0..36
    r = self.game.roulette
    best_net = best_n = None
    worst_net = worst_n = None
    for n in range(37):
        color = self._couleur_pour_numero_ROULETTE(n)
        net = sum(r.gain_pour_mise_ROULETTE(b, n, color) for b in self.game.bets)
        if best_net is None or net > best_net: best_net, best_n = net, n
        if worst_net is None or net < worst_net: worst_net, worst_n = net, n

    text = " | ".join(parts)
    text += f"\nMeilleur cas: {best_net:+.2f}€ (numéro {best_n}) — Pire cas: {worst_net:+.2f}€ (numéro {worst_n}) — Mises: {total_stake:.2f}€"
    self.potential_var.set(text)

# roulette_table_gui_carre_fr.py
# Roulette européenne — table centrée, carrés cliquables, jetons centrés,
# mode suppression de jetons, historique en bas.
# Toutes les fonctions sont francisées et suffixées par _ROULETTE.

import random
import tkinter as tk
from tkinter import ttk, messagebox

# ---------- Modèle ----------

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

    def tirer_ROULETTE(self):
        n = random.choice(self.pockets)
        color = 'green' if n == 0 else ('red' if n in self.red_numbers else 'black')
        return n, color

    def gain_pour_mise_ROULETTE(self, bet, outcome_number, outcome_color):
        """
        Paiements standard :
          - number: 35:1
          - red/black, even/odd, low/high: 1:1
          - dozen/column: 2:1
          - corner: 8:1
        Retourne le gain net (positif ou négatif).
        """
        t = bet.type
        a = bet.amount
        n = outcome_number

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
            raise ValueError("Type de mise inconnu: " + str(t))

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
    """Bankroll + liste des mises (fusion par (type, selection))."""
    def __init__(self, bankroll=500.0):
        self.roulette = Roulette()
        self.bankroll = float(bankroll)
        self.bets = []

    def mise_totale_ROULETTE(self):
        return sum(b.amount for b in self.bets)

    def ajouter_ou_fusionner_mise_ROULETTE(self, bet):
        if bet.amount <= 0:
            return "Montant invalide (<= 0)."
        if self.mise_totale_ROULETTE() + bet.amount > self.bankroll:
            return "Total des mises dépasserait la bankroll."

        t = bet.type
        if t == 'number':
            if bet.selection is None or not (0 <= int(bet.selection) <= 36):
                return "Numéro hors 0-36."
            bet.selection = int(bet.selection)
        elif t in ('dozen', 'column'):
            if bet.selection not in (1, 2, 3):
                return "Sélection doit être 1, 2 ou 3."
        elif t == 'corner':
            try:
                nums = tuple(sorted(int(x) for x in bet.selection))
            except Exception:
                return "Sélection de carré invalide."
            if len(nums) != 4:
                return "Un carré couvre 4 numéros."
            bet.selection = nums
        else:
            bet.selection = None

        for b in self.bets:
            if b.type == bet.type and b.selection == bet.selection:
                b.amount += bet.amount
                return None

        self.bets.append(bet)
        return None

    def supprimer_mise_par_cle_ROULETTE(self, key):
        """key = (type, selection normalisée). Supprime la mise fusionnée pour cette zone."""
        typ, sel = key
        for i, b in enumerate(self.bets):
            ksel = b.selection if b.type != 'corner' else tuple(sorted(b.selection))
            if b.type == typ and ksel == sel:
                del self.bets[i]
                return True
        return False

    def effacer_mises_ROULETTE(self):
        self.bets = []

    def lancer_et_regler_ROULETTE(self):
        if not self.bets:
            return "Aucune mise en attente."
        total_stake = self.mise_totale_ROULETTE()
        if total_stake > self.bankroll:
            return "Total des mises supérieur à la bankroll."
        n, color, results, net = self.roulette.regler_ROULETTE(self.bets)
        self.bankroll += net
        self.bets = []
        return n, color, results, net, self.bankroll

# ---------- Vue/Table (Canvas cliquable centré) ----------

class TableCanvas(tk.Canvas):
    """
    Canvas qui dessine la table (centrée), gère clics pour miser, et jetons cliquables.
    - Zones 'area:<type>:<selection?>' (cases, douzaines, colonnes, chances simples, corners)
    - Jetons taggés 'chip:<type>:<selection?>' (ovale + texte)
    """
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.config(highlightthickness=0)
        self.cell_w = 50
        self.cell_h = 40
        self.y0 = 20
        self.zero_w = 60
        self.side_w = 60
        self.x0 = 0  # calculé pour centrer
        self.areas = {}              # (type, selection) -> (x1,y1,x2,y2)
        self.chips = {}              # (type, selection) -> (oval_id, text_id)
        self.chip_item_to_key = {}   # item_id -> (type, selection)
        self.construire_table_ROULETTE()
        self.bind("<Button-1>", self._au_clic_ROULETTE)
        self.bind("<Configure>", lambda e: self._reconstruire_centre_ROULETTE())

    # ---------- Construction ----------

    def _taille_contenu_ROULETTE(self):
        cw, ch = self.cell_w, self.cell_h
        content_w = self.zero_w + 12*cw + self.side_w
        content_h = 3*ch + ch + ch
        return content_w, content_h

    def _calculer_x0_centre_ROULETTE(self):
        w = int(float(self.cget("width"))) if self.cget("width") else self.winfo_width()
        content_w, _ = self._taille_contenu_ROULETTE()
        left = max(10, (w - content_w) // 2)
        return left + self.zero_w

    def _reconstruire_centre_ROULETTE(self):
        self.delete("all")
        self.areas.clear()
        self.chips.clear()
        self.chip_item_to_key.clear()
        self.construire_table_ROULETTE()
        self.rafraichir_jetons_ROULETTE(self.app.game.bets)

    def construire_table_ROULETTE(self):
        cw, ch = self.cell_w, self.cell_h
        self.x0 = self._calculer_x0_centre_ROULETTE()
        x0, y0 = self.x0, self.y0
        zero_w, side_w = self.zero_w, self.side_w

        # Fond
        content_w, content_h = self._taille_contenu_ROULETTE()
        total_left = x0 - zero_w
        total_top  = y0
        total_right = x0 - zero_w + content_w
        total_bottom = y0 + content_h
        self.create_rectangle(total_left-10, total_top-10, total_right+10, total_bottom+10,
                              fill="#0a5f0a", outline="")

        # 0 vertical
        zx1, zy1 = x0 - zero_w, y0
        zx2, zy2 = x0, y0 + 3*ch
        self._rectangle_avec_libelle_ROULETTE(zx1, zy1, zx2, zy2, "0", fill="#0a990a",
                                              tag_type="number", selection=0, txt_color="white")

        # Grille 1-36
        numbers_map = {
            0: [3*(c+1) for c in range(12)],     # haut: 3,6,...,36
            1: [2 + 3*c for c in range(12)],     # milieu: 2,5,...,35
            2: [1 + 3*c for c in range(12)],     # bas: 1,4,...,34
        }
        red_set = self.app.game.roulette.red_numbers

        for r in range(3):
            for c in range(12):
                n = numbers_map[r][c]
                x1 = x0 + c*cw
                y1 = y0 + r*ch
                x2 = x1 + cw
                y2 = y1 + ch
                is_red = n in red_set
                fill = "#b80000" if is_red else "#111111"
                self._rectangle_avec_libelle_ROULETTE(x1, y1, x2, y2, str(n), fill=fill,
                                                      tag_type="number", selection=n, txt_color="white")

        # Colonnes 2:1 (droite)
        for r, col_sel in [(0,3), (1,2), (2,1)]:
            x1 = x0 + 12*cw
            y1 = y0 + r*ch
            x2 = x1 + side_w
            y2 = y1 + ch
            self._rectangle_avec_libelle_ROULETTE(x1, y1, x2, y2, "2:1", fill="#0a990a",
                                                  tag_type="column", selection=col_sel, txt_color="white")

        # Douzaines
        dy = y0 + 3*ch
        labels = ["1st 12", "2nd 12", "3rd 12"]
        for i, lab in enumerate(labels, start=1):
            x1 = x0 + (i-1)*4*cw
            y1 = dy
            x2 = x1 + 4*cw
            y2 = y1 + ch
            self._rectangle_avec_libelle_ROULETTE(x1, y1, x2, y2, lab, fill="#0a990a",
                                                  tag_type="dozen", selection=i, txt_color="white")

        # Chances simples
        by = dy + ch
        outs = [
            ("low",  "1-18"),
            ("even", "PAIR"),
            ("red",  "ROUGE"),
            ("black","NOIR"),
            ("odd",  "IMPAIR"),
            ("high", "19-36")
        ]
        for i, (typ, lab) in enumerate(outs):
            x1 = x0 + i*2*cw
            y1 = by
            x2 = x1 + 2*cw
            y2 = y1 + ch
            fill = "#b80000" if typ == "red" else ("#111111" if typ == "black" else "#0a990a")
            self._rectangle_avec_libelle_ROULETTE(x1, y1, x2, y2, lab, fill=fill,
                                                  tag_type=typ, selection=None, txt_color="white")

        # Carrés (corners) : intersections 2x2
        corner_radius = 12
        for r in (0, 1):
            for c in range(11):
                tl = numbers_map[r][c]
                tr = numbers_map[r][c+1]
                bl = numbers_map[r+1][c]
                br = numbers_map[r+1][c+1]
                nums = tuple(sorted((tl, tr, bl, br)))
                cx = x0 + (c+1)*cw
                cy = y0 + (r+1)*ch
                x1 = cx - corner_radius
                y1 = cy - corner_radius
                x2 = cx + corner_radius
                y2 = cy + corner_radius
                self.create_polygon(
                    cx, y1, x2, cy, cx, y2, x1, cy,
                    fill="#e5d100", outline="black", width=1,
                    tags=(self._tag_carre_ROULETTE(nums), "area")
                )
                self.areas[("corner", nums)] = (x1, y1, x2, y2)

    # ---------- Outils de dessin / tags ----------

    def _rectangle_avec_libelle_ROULETTE(self, x1, y1, x2, y2, text, fill, tag_type, selection, txt_color="white"):
        sel_str = "" if selection is None else (str(selection) if not isinstance(selection, (tuple, list, set))
                                               else "_".join(str(x) for x in selection))
        tag = f"area:{tag_type}:{sel_str}"
        self.create_rectangle(x1, y1, x2, y2, fill=fill, outline="white", width=1, tags=(tag, "area"))
        tx = (x1 + x2) / 2
        ty = (y1 + y2) / 2
        self.create_text(tx, ty, text=text, fill=txt_color, font=("Arial", 12, "bold"), tags=(tag, "area"))
        self.areas[(tag_type, selection)] = (x1, y1, x2, y2)

    def _tag_carre_ROULETTE(self, nums_tuple):
        return "area:corner:" + "_".join(str(x) for x in nums_tuple)

    # ---------- Interaction ----------

    def _au_clic_ROULETTE(self, event):
        items = self.find_overlapping(event.x, event.y, event.x, event.y)
        delete_mode = self.app.delete_mode_var.get()

        # 1) Priorité aux jetons si mode suppression activé
        if delete_mode:
            key = self._cle_depuis_jeton_ROULETTE(items)
            if key is not None:
                removed = self.app.supprimer_mise_par_cle_ROULETTE(key)
                if removed:
                    self.rafraichir_jetons_ROULETTE(self.app.game.bets)
                return  # en mode suppression, on ne pose pas de mise

        # 2) Sinon, chercher une zone de mise 'area:*'
        key = self._cle_depuis_zone_ROULETTE(items)
        if key:
            self.app.placer_mise_depuis_table_ROULETTE(key)

    def _cle_depuis_jeton_ROULETTE(self, items):
        """Renvoie (type, selection) si un jeton est cliqué (top-most d'abord)."""
        for it in reversed(items):  # top-most
            tags = self.gettags(it)
            for t in tags:
                if t.startswith("chip:"):
                    _, typ, sel_str = t.split(":", 2)
                    if typ == "corner":
                        try:
                            sel = tuple(sorted(int(x) for x in sel_str.split("_") if x))
                        except Exception:
                            sel = None
                    else:
                        if sel_str == "":
                            sel = None
                        else:
                            try:
                                sel = int(sel_str)
                            except ValueError:
                                sel = None
                    return (typ, sel)
        return None

    def _cle_depuis_zone_ROULETTE(self, items):
        """Renvoie (type, selection) à partir des zones 'area:*' (top-most prioritaire)."""
        for it in reversed(items):  # top-most
            tags = self.gettags(it)
            for t in tags:
                if not t.startswith("area:"):
                    continue
                _, typ, sel = t.split(":", 2)
                if typ == "corner":
                    try:
                        selection = tuple(sorted(int(x) for x in sel.split("_") if x))
                    except Exception:
                        selection = None
                else:
                    if sel == "":
                        selection = None
                    else:
                        try:
                            selection = int(sel)
                        except ValueError:
                            selection = None
                return (typ, selection)
        return None

    # ----- Jetons (affichage montants) -----

    def rafraichir_jetons_ROULETTE(self, bets):
        # supprimer anciens jetons
        for ids in list(self.chips.values()):
            for i in ids:
                self.delete(i)
        self.chips.clear()
        self.chip_item_to_key.clear()

        # agrégation (type, selection)
        agg = {}
        for b in bets:
            ksel = b.selection if b.type != 'corner' else tuple(sorted(b.selection))
            k = (b.type, ksel)
            agg[k] = agg.get(k, 0.0) + b.amount

        # dessiner jetons centrés
        for key, amount in agg.items():
            if key not in self.areas:
                continue
            x1, y1, x2, y2 = self.areas[key]
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            r = 12
            tags = self._tags_jeton_pour_cle_ROULETTE(key)
            oval = self.create_oval(cx - r, cy - r, cx + r, cy + r,
                                    fill="white", outline="black", width=1,
                                    tags=tags)
            val = int(amount) if float(amount).is_integer() else round(amount, 2)
            txt = self.create_text(cx, cy, text=f"{val}", fill="black",
                                   font=("Arial", 9, "bold"),
                                   tags=tags)
            self.chips[key] = (oval, txt)
            self.chip_item_to_key[oval] = key
            self.chip_item_to_key[txt] = key

    def _tags_jeton_pour_cle_ROULETTE(self, key):
        typ, sel = key
        if typ == "corner":
            sel_str = "_".join(str(x) for x in sel)
        else:
            sel_str = "" if sel is None else str(sel)
        return ("chip", f"chip:{typ}:{sel_str}")

# ---------- Application ----------

class RouletteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Roulette (EU) — Table, Carrés, Jetons centrés, Suppression")
        self.resizable(False, False)

        self.game = Game(bankroll=500.0)

        # Variables UI
        self.click_amount_var = tk.StringVar(value="10")
        self.delete_mode_var = tk.BooleanVar(value=False)

        # UI
        self.construire_barre_haut_ROULETTE()
        self.construire_table_ROULETTE()
        self.construire_historique_bas_ROULETTE()

        self.maj_bankroll_ROULETTE()
        self.journaliser_ROULETTE("Cliquez pour miser. Activez 'Suppression jetons' pour retirer des mises en cliquant sur les jetons.")

    # ---- UI ----

    def construire_barre_haut_ROULETTE(self):
        top = ttk.Frame(self, padding=10)
        top.grid(row=0, column=0, sticky="ew")

        ttk.Label(top, text="Bankroll:").grid(row=0, column=0, sticky="w")
        self.bankroll_lbl = ttk.Label(top, text="0.00")
        self.bankroll_lbl.grid(row=0, column=1, padx=(6,20))

        ttk.Label(top, text="Montant par clic:").grid(row=0, column=2)
        self.amount_entry = ttk.Entry(top, textvariable=self.click_amount_var, width=8)
        self.amount_entry.grid(row=0, column=3, padx=6)

        # Bouton toggle suppression des jetons
        self.delete_chk = ttk.Checkbutton(top, text="Suppression jetons",
                                          variable=self.delete_mode_var,
                                          command=self.basculer_mode_suppr_ROULETTE)
        self.delete_chk.grid(row=0, column=4, padx=(15,0))

        ttk.Button(top, text="Lancer (spin)", command=self.lancer_ROULETTE).grid(row=0, column=5, padx=(20,0))

        ttk.Label(top, text="Dernier tirage:").grid(row=0, column=6, padx=(20,6))
        self.outcome_lbl = ttk.Label(top, text="—")
        self.outcome_lbl.grid(row=0, column=7)

    def construire_table_ROULETTE(self):
        frame = ttk.Frame(self, padding=(10,0,10,10))
        frame.grid(row=1, column=0, sticky="n")
        self.table = TableCanvas(frame, self, width=900, height=360, bg="#084f08")
        self.table.pack()

    def construire_historique_bas_ROULETTE(self):
        box = ttk.LabelFrame(self, text="Historique", padding=10)
        box.grid(row=2, column=0, padx=10, pady=(0,10), sticky="ew")
        self.history = tk.Text(box, width=120, height=12, state="disabled")
        self.history.grid(row=0, column=0)

    # ---- Utilitaires ----

    def basculer_mode_suppr_ROULETTE(self):
        if self.delete_mode_var.get():
            self.table.config(cursor="pirate")
            self.journaliser_ROULETTE("[Mode] Suppression jetons: ON (cliquez un jeton pour supprimer la mise)")
        else:
            self.table.config(cursor="")
            self.journaliser_ROULETTE("[Mode] Suppression jetons: OFF")

    def maj_bankroll_ROULETTE(self):
        self.bankroll_lbl.config(text=f"{self.game.bankroll:.2f}")

    def journaliser_ROULETTE(self, text):
        self.history.config(state="normal")
        self.history.insert("end", text + "\n")
        self.history.see("end")
        self.history.config(state="disabled")

    def formater_selection_ROULETTE(self, sel):
        if isinstance(sel, (tuple, list, set)):
            return " " + "-".join(str(x) for x in sel)
        return "" if sel is None else f" {sel}"

    # ---- Actions ----

    def placer_mise_depuis_table_ROULETTE(self, key):
        if self.delete_mode_var.get():
            return
        typ, selection = key
        amt_txt = self.click_amount_var.get().replace(",", ".").strip()
        try:
            amount = float(amt_txt)
        except ValueError:
            messagebox.showerror("Montant", "Montant par clic invalide.")
            return

        if typ == 'corner' and isinstance(selection, (tuple, list, set)):
            selection = tuple(sorted(int(x) for x in selection))

        bet = Bet(typ, selection, amount)
        err = self.game.ajouter_ou_fusionner_mise_ROULETTE(bet)
        if err:
            messagebox.showwarning("Mise refusée", err)
            return

        self.table.rafraichir_jetons_ROULETTE(self.game.bets)

    def supprimer_mise_par_cle_ROULETTE(self, key):
        removed = self.game.supprimer_mise_par_cle_ROULETTE(key)
        if removed:
            self.journaliser_ROULETTE(f"Suppression mise -> {key[0]}{self.formater_selection_ROULETTE(key[1])}")
            self.table.rafraichir_jetons_ROULETTE(self.game.bets)
        return removed

    def lancer_ROULETTE(self):
        res = self.game.lancer_et_regler_ROULETTE()
        if isinstance(res, str):
            messagebox.showwarning("Impossible de lancer", res)
            return

        n, color, results, net, bank = res
        color_fr = {"red": "Rouge", "black": "Noir", "green": "Vert"}[color]
        self.outcome_lbl.config(text=f"{n} ({color_fr})")
        self.maj_bankroll_ROULETTE()

        # Vider les jetons (mises consommées)
        self.table.rafraichir_jetons_ROULETTE(self.game.bets)

        self.journaliser_ROULETTE(f"Sortie: {n} ({color_fr})")
        for b, gain in results:
            self.journaliser_ROULETTE(f" - {b.type}{self.formater_selection_ROULETTE(b.selection)} mise {b.amount:.2f}: {'gagné' if gain>0 else 'perdu'} -> {gain:+.2f}")
        self.journaliser_ROULETTE(f"Net: {net:+.2f} | Bankroll: {bank:.2f}")
        self.journaliser_ROULETTE("-"*54)

# ---------- Lancement ----------

if __name__ == "__main__":
    try:
        app = RouletteApp()
        app.mainloop()
    except Exception as e:
        print("Erreur au lancement de l'application :", e)

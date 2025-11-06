
import random

class Bet:
    """Mise (type, selection, amount). selection: int/None/tuple(int,int,int,int) pour 'corner'."""
    def __init__(self, type_, selection, amount):
        self.type = str(type_).lower()
        self.selection = selection
        self.amount = float(amount)

class Roulette:
    """Roulette européenne (0-36, un seul zéro)."""
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
        Règles de paiement :
          - number (plein) : 35:1
          - red/black, even/odd, low/high : 1:1
          - dozen/column : 2:1
          - corner (carré 4 numéros) : 8:1
        Retourne le gain NET (peut être négatif).
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
    """Gestion bankroll + liste des mises (fusion par (type, selection))."""
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

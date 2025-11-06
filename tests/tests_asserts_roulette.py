import Roulette as mod


def _color_for(n, red_set):
    """Couleur logique d'un numéro pour alimenter les tests de paiement."""
    return "green" if n == 0 else ("red" if n in red_set else "black")


def tests_roulette_payouts():
    r = mod.Roulette()
    red = r.red_numbers

    # --- Number (plein) 35:1 ---
    bet = mod.Bet("number", 17, 10)
    assert r.gain_pour_mise_ROULETTE(bet, 17, _color_for(17, red)) == 350  # gagne 35:1 sur 17
    assert r.gain_pour_mise_ROULETTE(bet, 18, _color_for(18, red)) == -10  # perd si autre numéro

    # --- Red / Black (1:1) ---
    bet_red = mod.Bet("red", None, 10)
    assert r.gain_pour_mise_ROULETTE(bet_red, 18, _color_for(18, red)) == 10   # 18 rouge -> gagne
    assert r.gain_pour_mise_ROULETTE(bet_red, 17, _color_for(17, red)) == -10  # 17 noir -> perd

    bet_black = mod.Bet("black", None, 10)
    assert r.gain_pour_mise_ROULETTE(bet_black, 17, _color_for(17, red)) == 10  # 17 noir -> gagne
    assert r.gain_pour_mise_ROULETTE(bet_black, 18, _color_for(18, red)) == -10  # 18 rouge -> perd

    # --- Even / Odd (1:1), 0 perd ---
    bet_even = mod.Bet("even", None, 10)
    assert r.gain_pour_mise_ROULETTE(bet_even, 18, _color_for(18, red)) == 10   # 18 pair -> gagne
    assert r.gain_pour_mise_ROULETTE(bet_even, 17, _color_for(17, red)) == -10  # 17 impair -> perd
    assert r.gain_pour_mise_ROULETTE(bet_even, 0, "green") == -10               # 0 -> perd sur pair

    bet_odd = mod.Bet("odd", None, 10)
    assert r.gain_pour_mise_ROULETTE(bet_odd, 17, _color_for(17, red)) == 10    # 17 impair -> gagne
    assert r.gain_pour_mise_ROULETTE(bet_odd, 18, _color_for(18, red)) == -10   # 18 pair -> perd

    # --- Low / High (1:1) ---
    bet_low = mod.Bet("low", None, 10)
    assert r.gain_pour_mise_ROULETTE(bet_low, 1, _color_for(1, red)) == 10      # 1-18 -> gagne
    assert r.gain_pour_mise_ROULETTE(bet_low, 19, _color_for(19, red)) == -10   # 19-36 -> perd

    bet_high = mod.Bet("high", None, 10)
    assert r.gain_pour_mise_ROULETTE(bet_high, 36, _color_for(36, red)) == 10   # 19-36 -> gagne
    assert r.gain_pour_mise_ROULETTE(bet_high, 18, _color_for(18, red)) == -10  # 1-18 -> perd

    # --- Dozens (2:1) ---
    bet_d1 = mod.Bet("dozen", 1, 10)
    assert r.gain_pour_mise_ROULETTE(bet_d1, 1, _color_for(1, red)) == 20       # 1..12 -> gagne 2:1
    assert r.gain_pour_mise_ROULETTE(bet_d1, 13, _color_for(13, red)) == -10    # hors douzaine -> perd

    bet_d2 = mod.Bet("dozen", 2, 10)
    assert r.gain_pour_mise_ROULETTE(bet_d2, 13, _color_for(13, red)) == 20     # 13..24 -> gagne

    bet_d3 = mod.Bet("dozen", 3, 10)
    assert r.gain_pour_mise_ROULETTE(bet_d3, 30, _color_for(30, red)) == 20     # 25..36 -> gagne

    # --- Columns (2:1) ---
    # Rappel: (n-1)%3 == 0 -> col 1 ; ==1 -> col 2 ; ==2 -> col 3
    bet_c1 = mod.Bet("column", 1, 10)
    assert r.gain_pour_mise_ROULETTE(bet_c1, 4, _color_for(4, red)) == 20       # 4 en colonne 1 -> gagne
    assert r.gain_pour_mise_ROULETTE(bet_c1, 5, _color_for(5, red)) == -10      # 5 pas en col 1 -> perd

    bet_c2 = mod.Bet("column", 2, 10)
    assert r.gain_pour_mise_ROULETTE(bet_c2, 5, _color_for(5, red)) == 20       # 5 en colonne 2 -> gagne

    bet_c3 = mod.Bet("column", 3, 10)
    assert r.gain_pour_mise_ROULETTE(bet_c3, 6, _color_for(6, red)) == 20       # 6 en colonne 3 -> gagne

    # --- Corner (carré) 8:1 ---
    bet_corner = mod.Bet("corner", (1, 2, 4, 5), 10)
    assert r.gain_pour_mise_ROULETTE(bet_corner, 4, _color_for(4, red)) == 80   # 4 est dans le carré -> 8:1
    assert r.gain_pour_mise_ROULETTE(bet_corner, 6, _color_for(6, red)) == -10  # hors carré -> perd


def tests_game_flow_and_validation():
    g = mod.Game(bankroll=100)

    # --- mise_totale_ROULETTE ---
    assert g.mise_totale_ROULETTE() == 0                            # au départ, total des mises = 0

    # --- ajouter_ou_fusionner_mise_ROULETTE (ajout) ---
    err = g.ajouter_ou_fusionner_mise_ROULETTE(mod.Bet("number", 5, 10))
    assert err is None                                              # ajout d'une mise valide -> pas d'erreur
    assert g.mise_totale_ROULETTE() == 10                           # total des mises mis à jour
    assert len(g.bets) == 1 and g.bets[0].selection == 5            # une seule mise, sur le numéro 5

    # --- fusion sur la même zone ---
    err = g.ajouter_ou_fusionner_mise_ROULETTE(mod.Bet("number", 5, 15))
    assert err is None                                              # fusion autorisée pour même (type, selection)
    assert len(g.bets) == 1 and g.bets[0].amount == 25              # montant fusionné (10+15)=25
    assert g.mise_totale_ROULETTE() == 25                           # total des mises reflète la fusion

    # --- ajout d'un carré valide ---
    err = g.ajouter_ou_fusionner_mise_ROULETTE(mod.Bet("corner", (1, 2, 4, 5), 10))
    assert err is None                                              # carré (4 numéros) valide -> accepté
    assert len(g.bets) == 2                                         # 2 zones maintenant

    # --- validation corner invalide (mauvaise taille) ---
    err = g.ajouter_ou_fusionner_mise_ROULETTE(mod.Bet("corner", (1, 2, 3), 10))
    assert isinstance(err, str)                                     # renvoie un message d'erreur texte

    # --- rejet si dépassement de bankroll (cumul) ---
    g2 = mod.Game(bankroll=20)
    assert g2.ajouter_ou_fusionner_mise_ROULETTE(mod.Bet("red", None, 15)) is None   # 15 accepté
    err2 = g2.ajouter_ou_fusionner_mise_ROULETTE(mod.Bet("black", None, 10))         # 15+10>20
    assert isinstance(err2, str)                                                      # rejet car dépasse

    # --- suppression par clé ---
    removed = g.supprimer_mise_par_cle_ROULETTE(("number", 5))
    assert removed is True                                           # supprime la mise plein sur 5
    assert len(g.bets) == 1                                          # il ne reste que le corner

    # --- suppression d'une clé inexistante ---
    assert g.supprimer_mise_par_cle_ROULETTE(("number", 17)) is False  # rien à supprimer -> False

    # --- effacer_mises_ROULETTE ---
    g.effacer_mises_ROULETTE()
    assert g.bets == []                                              # liste des mises vidée

    # --- lancer_et_regler_ROULETTE -> message si aucune mise ---
    res = g.lancer_et_regler_ROULETTE()
    assert isinstance(res, str)                                      # pas de mise => renvoie un texte explicatif

    # --- lancer_et_regler_ROULETTE avec tirage "mocké" ---
    # On fixe le tirage de Roulette pour ce test à (18, 'red') afin d'être déterministe.
    original_tirer = mod.Roulette.tirer_ROULETTE
    mod.Roulette.tirer_ROULETTE = lambda self: (18, "red")           # patch: tirage constant

    try:
        g3 = mod.Game(bankroll=100)
        assert g3.ajouter_ou_fusionner_mise_ROULETTE(mod.Bet("even", None, 10)) is None  # pair -> gagnera
        assert g3.ajouter_ou_fusionner_mise_ROULETTE(mod.Bet("black", None, 5)) is None  # noir -> perdra
        assert g3.ajouter_ou_fusionner_mise_ROULETTE(mod.Bet("number", 18, 1)) is None   # plein gagnant 35:1

        res2 = g3.lancer_et_regler_ROULETTE()
        assert isinstance(res2, tuple) and len(res2) == 5             # résultat forme: (n, color, results, net, bank)
        n, color, results, net, bank = res2
        assert (n, color) == (18, "red")                              # tirage mocké respecté
        assert net == 40                                              # +10 (even) -5 (black) +35 (plein 1u) = +40
        assert bank == 140.0                                          # bankroll mise à jour 100 + 40
        assert g3.bets == []                                          # les mises sont vidées après règlement
    finally:
        mod.Roulette.tirer_ROULETTE = original_tirer                  # on rétablit le vrai tirage


if __name__ == "__main__":
    # Lance l’ensemble des tests/asserts
    tests_roulette_payouts()
    tests_game_flow_and_validation()
    print("Tous les asserts ont réussi : la logique du jeu fonctionne comme attendu.")

# test_ui_roulette_asserts.py
# Tests "maison" (sans pytest) pour ui_roulette_fr.py
# On évite d'afficher la fenêtre en utilisant withdraw(), et on détruit à la fin.

import tkinter as tk
import ui_roulette as ui
import modele_roulette as mod

def tests_ui_ROULETTE():
    # Mock du tirage pour un test déterministe
    original = mod.Roulette.tirer_ROULETTE
    mod.Roulette.tirer_ROULETTE = lambda self: (18, "red")

    app = ui.RouletteApp()
    app.withdraw()  # pas d'affichage de fenêtre

    try:
        # --- La table existe et contient des zones clés ---
        areas = app.table.areas
        assert ("number", 17) in areas              # case 17 présente
        assert ("dozen", 1) in areas                # 1st 12 présente
        assert ("column", 3) in areas               # colonne 3 présente
        assert ("corner", (1,2,4,5)) in areas       # un carré typique présent

        # --- Placer des mises via l'API UI ---
        app.click_amount_var.set("10")
        app.placer_mise_depuis_table_ROULETTE(("even", None))   # gagne
        app.placer_mise_depuis_table_ROULETTE(("black", None))  # perd

        app.click_amount_var.set("1")
        app.placer_mise_depuis_table_ROULETTE(("number", 18))   # plein gagnant

        # --- Vérifier que des jetons sont dessinés et centrés (ex: number 18) ---
        key = ("number", 18)
        app.table.rafraichir_jetons_ROULETTE(app.game.bets)
        assert key in app.table.chips
        oval_id, _txt_id = app.table.chips[key]
        x1, y1, x2, y2 = app.table.areas[key]
        cx_zone = (x1 + x2) / 2
        cy_zone = (y1 + y2) / 2
        ox1, oy1, ox2, oy2 = app.table.coords(oval_id)
        cx_chip = (ox1 + ox2) / 2
        cy_chip = (oy1 + oy2) / 2
        assert abs(cx_chip - cx_zone) < 0.1 and abs(cy_chip - cy_zone) < 0.1  # jeton centré

        # --- Lancer un coup via l'UI et vérifier la bankroll ---
        app.game.bankroll = 100.0
        app.lancer_ROULETTE()
        assert float(app.game.bankroll) == 140.0    # +40 comme dans le test logique

        # --- Mode suppression : cocher et supprimer un jeton ---
        app.click_amount_var.set("5")
        app.placer_mise_depuis_table_ROULETTE(("red", None))
        assert any(b.type == "red" for b in app.game.bets)

        app.delete_mode_var.set(True)
        removed = app.supprimer_mise_par_cle_ROULETTE(("red", None))
        assert removed is True
        assert not any(b.type == "red" for b in app.game.bets)

        # --- L'historique s'alimente (au moins 1 ligne) ---
        txt = app.history.get("1.0", "end").strip()
        assert len(txt) > 0

    finally:
        app.destroy()
        mod.Roulette.tirer_ROULETTE = original

if __name__ == "__main__":
    tests_ui_ROULETTE()
    print("✅ Tests UI OK")

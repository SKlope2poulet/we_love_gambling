# test_gain_potentiel_asserts.py
# Vérifie la ligne "Gains potentiels" via asserts (sans pytest).

import Roulette as jeu

def test_gain_potentiel():
    app = jeu.RouletteApp()
    app.withdraw()  # évite d'afficher la fenêtre

    try:
        # Place des mises : PAIR 10€ et Plein 18 à 1€
        app.click_amount_var.set("10")
        app.placer_mise_depuis_table_ROULETTE(("even", None))
        app.click_amount_var.set("1")
        app.placer_mise_depuis_table_ROULETTE(("number", 18))

        txt = app.potential_var.get()
        # Vérifs de base : lignes par mise
        assert "PAIR" in txt                    # présence de la mise "pair"
        assert "+10.00€" in txt                 # profit net attendu pour pair
        assert "Plein 18" in txt                # présence de la mise plein 18
        assert "+35.00€" in txt                 # profit net attendu pour plein 18

        # Vérif meilleurs/pires cas globaux
        assert "Meilleur cas: +45.00€" in txt   # 10 + 35 si 18 sort
        assert "Pire cas: -11.00€" in txt       # -10 (pair perd) -1 (plein perd)

        # Après un spin, la zone doit être réinitialisée
        app.lancer_ROULETTE()
        assert app.potential_var.get() == "—"

    finally:
        app.destroy()

if __name__ == "__main__":
    test_gain_potentiel()
    print("✅ Test gain potentiel OK")

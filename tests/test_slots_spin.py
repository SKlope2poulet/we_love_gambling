from src.games.slots import SlotMachineApp

def test_spin_modifie_les_reels():
    """US2: L'utilisateur lance un spin"""
    app = SlotMachineApp()
    avant = list(app.reels)
    app.spin()
    apres = list(app.reels)
    assert avant != apres, "Les rouleaux doivent changer après un spin."

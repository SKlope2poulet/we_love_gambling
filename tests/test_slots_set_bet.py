from src.games.slots import SlotMachineApp

def test_choisir_sa_mise():
    """US1: L'utilisateur peut définir sa mise"""
    app = SlotMachineApp()
    app.set_bet(10)
    assert app.current_bet == 10, "La mise de l'utilisateur doit être bien enregistrée."

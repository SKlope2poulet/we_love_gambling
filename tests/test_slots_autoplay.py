from src.games.slots import SlotMachineApp

def test_autoplay_fait_plusieurs_spins():
    """US3: L'utilisateur peut lancer plusieurs spins automatiquement"""
    app = SlotMachineApp()
    app.autoplay(rounds=5)
    assert app.total_spins == 5, "L’autoplay doit exécuter plusieurs spins."

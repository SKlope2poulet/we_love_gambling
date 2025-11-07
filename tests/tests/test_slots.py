import pytest
from src.games.slots import SlotMachineApp

@pytest.fixture
def app():
    return SlotMachineApp()

def test_mise_initiale_par_defaut(app):
    """Vérifie qu'une mise par défaut existe"""
    assert app.current_bet == 1, "La mise par défaut doit être de 1€"

def test_changer_mise(app):
    """Vérifie qu'on peut modifier la mise"""
    app.set_bet(5)
    assert app.current_bet == 5, "L'utilisateur doit pouvoir choisir sa mise"

def test_spin_lance_rouleaux(app):
    """Vérifie qu'un spin modifie les symboles"""
    avant = list(app.reels)
    app.spin()
    apres = list(app.reels)
    assert avant != apres, "Les rouleaux doivent changer après un spin"

def test_autoplay_fait_plusieurs_spins(app):
    """Vérifie que l'autoplay fait plusieurs tours"""
    app.reels_history.clear()
    app.autoplay(rounds=5)
    assert len(app.reels_history) == 5, "L'autoplay doit enregistrer plusieurs spins"

def test_recapitulatif_session(app):
    """Vérifie que le récapitulatif renvoie le bon format"""
    recap = app.get_session_summary()
    assert "total_spins" in recap and "rtp" in recap, "Le résumé de session doit contenir total_spins et rtp"

from src.ui.navbar import Navbar

def test_navbar_is_fixed():
    nav = Navbar()
    assert nav.is_fixed() is True
    assert "Accueil" in nav.links

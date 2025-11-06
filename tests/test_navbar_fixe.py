from src.ui.navbar import Navbar

def test_navbar_is_fixed():
    nav = Navbar()
    assert nav.fixed is True

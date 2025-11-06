from main import create_homepage

def test_homepage_structure():
    homepage = create_homepage()
    assert "navigation" in homepage
    assert "games" in homepage

from src.ui.legal_popup import LegalPopup

def test_legal_popup_contains_cgu():
    popup = LegalPopup()
    assert "CGU" in popup.text
    assert "confidentialité" in popup.text

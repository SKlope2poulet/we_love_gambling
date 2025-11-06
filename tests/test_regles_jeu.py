from src.ui.rules_page import RulesPage

def test_rules_page_content():
    page = RulesPage("Blackjack")
    assert "Blackjack" in page.rules

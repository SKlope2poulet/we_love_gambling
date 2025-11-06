from src.ui.balance_display import BalanceDisplay

def test_balance_initial_value():
    b = BalanceDisplay()
    assert b.balance == 1000  # solde initial fictif

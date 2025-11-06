from src.ui.portfolio import Portfolio

def test_deposit_and_withdraw():
    p = Portfolio()
    p.deposit(500)
    assert p.balance == 1500
    p.withdraw(200)
    assert p.balance == 1300

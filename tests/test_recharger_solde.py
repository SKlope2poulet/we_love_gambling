from src.ui.recharge_button import RechargeButton

def test_recharger_button_label():
    btn = RechargeButton()
    assert btn.label == "Recharger le solde"

from src.ui.fake_money_warning import FakeMoneyWarning

def test_message_content():
    msg = FakeMoneyWarning().message
    assert "aucune mise réelle" in msg

from blackjack import BlackjackGame

def test_double_hides_last_card():
    game = BlackjackGame(balance=200)
    game.start_hand(50)
    game.double(hide_card=True)
    assert game.last_card_hidden is True

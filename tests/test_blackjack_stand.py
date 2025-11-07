from blackjack import BlackjackGame

def test_stand_sets_state():
    game = BlackjackGame()
    game.start_hand(10)
    game.stand()
    assert game.state == "dealer_turn"

from blackjack import BlackjackGame

def test_start_hand_sets_bet_and_balance():
    game = BlackjackGame(balance=200)
    game.start_hand(50)
    assert game.bet == 50
    assert game.balance == 150

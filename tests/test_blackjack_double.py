from blackjack import BlackjackGame

def test_double_doubles_bet_and_draws_one():
    game = BlackjackGame(balance=200)
    game.start_hand(50)
    before = len(game.player_hand)
    game.double()
    assert game.bet == 100
    assert len(game.player_hand) == before + 1

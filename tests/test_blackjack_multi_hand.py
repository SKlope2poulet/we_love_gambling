from blackjack import BlackjackGame

def test_multiple_hands_can_be_played():
    game = BlackjackGame(balance=300)
    game.start_multiple_hands([10, 20, 30])
    assert len(game.hands) == 3
    assert sum(h["bet"] for h in game.hands) == 60
    assert game.balance == 240

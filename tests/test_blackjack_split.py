from blackjack import BlackjackGame

def test_split_creates_two_hands_when_pair():
    game = BlackjackGame(balance=200)
    game.player_hand = [("8", 8), ("8", 8)]
    game.bet = 50
    game.split()
    assert len(game.hands) == 2
    assert all(len(h) == 1 for h in game.hands)

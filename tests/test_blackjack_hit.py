def test_hit_adds_card():
    game = BlackjackGame()
    game.start_hand(10)
    before = len(game.player_hand)
    game.hit()
    assert len(game.player_hand) == before + 1

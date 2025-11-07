def test_autoplay_runs_multiple_rounds(monkeypatch):
    game = BlackjackGame()
    called = {"count": 0}
    def fake_round(): called["count"] += 1
    game.play_round = fake_round
    game.autoplay(3)
    assert called["count"] == 3


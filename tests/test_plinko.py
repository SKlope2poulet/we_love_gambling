import pytest
from src.games.plinko import Plinko

def test_play_reduces_balance_and_gives_result(monkeypatch):
    game = Plinko("moyen")
    initial_balance = game.balance

    # on force le slot pour test déterministe
    monkeypatch.setattr("random.randint", lambda a, b: 2)

    result = game.play(10)

    assert "gain" in result
    assert "multiplier" in result
    assert "balance" in result
    assert result["balance"] <= initial_balance + 100  # sécurité
    assert isinstance(result["multiplier"], (int, float))

def test_invalid_bet_raises_error():
    game = Plinko("facile")

    with pytest.raises(ValueError):
        game.play(-5)

    with pytest.raises(ValueError):
        game.play(game.balance + 10)

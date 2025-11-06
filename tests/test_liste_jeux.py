from src.ui.game_list import GameList

def test_game_list_initialization():
    gl = GameList()
    assert isinstance(gl.games, list)

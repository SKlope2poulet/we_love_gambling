from src.ui.dashboard import Dashboard

def test_dashboard_kpi_calculation():
    d = Dashboard(wins=5, losses=5)
    assert d.win_rate() == 50

from src.games.slots import SlotMachineApp

def test_recapitulatif_session():
    """US4: Récapitulatif des mises, gains et RTP"""
    app = SlotMachineApp()
    app.set_bet(2)
    app.autoplay(10)
    recap = app.get_session_summary()
    assert "total_spins" in recap
    assert "rtp" in recap

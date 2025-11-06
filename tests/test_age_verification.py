from src.ui.age_verification import AgeVerification

def test_user_major():
    av = AgeVerification()
    assert av.is_of_age(18) is True
    assert av.is_of_age(16) is False

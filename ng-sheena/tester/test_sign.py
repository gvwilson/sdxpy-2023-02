from sign import sign

def test_sign_negative():
    assert sign(-5) == -1

def test_sign_positive():
    assert sign(20) == 1

def test_sign_zero():
    """test:assert"""
    assert sign(0) == 0

def test_sign_error():
    assert sgn(-5) == -1
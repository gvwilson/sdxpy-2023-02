from sign import sign


def test_sign_negative():
    assert sign(-3) == -1


def test_sign_positive():
    assert sign(19) == 1


def test_sign_zero():
    """test:assert"""
    assert sign(0) == 0


# Misspelled 'sign'
def test_sign_error():
    assert sgn(1) == 1


test_sign_error.skip = True

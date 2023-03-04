# Should return 0 when given 0

def sign(value):
    if value < 0:
        return -1
    else:
        return 1


def test_sign_negative():
    assert sign(-3) == -1


def test_sign_positive():
    assert sign(19) == 1


def test_sign_zero():
    assert sign(0) == 0


# Misspelled 'sign'
def test_sign_error():
    assert sgn(1) == 1
    
def setup():

    print("I have done some complicated setup!")


def teardown():
    print("I have undone the complicated teardown!")

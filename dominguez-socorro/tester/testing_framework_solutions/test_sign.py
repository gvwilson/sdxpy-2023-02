# copied from slides
# https://third-bit.com//sdxpy/tester/slides/#23
from sign import sign

def test_sign_negative():
    assert sign(-3) == -1
def test_sign_positive():
    assert sign(19) == 1
def test_sign_zero():
    assert sign(0) == 0
def test_sign_error():
    assert sgn(1) == 1
    
def test_sign_assert():
    '''test:assert'''
    assert sign(1) == 1 

def test_sign_assert2():
    '''test:assert'''
    assert sign(3) == 2
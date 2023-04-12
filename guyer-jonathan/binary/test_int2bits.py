from int2bits import int2bits, bits2int

def test_10_2bits():
    assert int2bits(10) == "1010"

def test_0_2bits():
    assert int2bits(0) == "0"

def test_65535_2bits():
    assert int2bits(65535) == "1111111111111111"

def test_1010_2int():
    assert bits2int("1010") == 10

def test_0_2int():
    assert bits2int("0") == 0

def test_1111111111111111_2int():
    assert bits2int("1111111111111111") == 65535

def test_0000_2int():
    assert bits2int("0000") == 0

def test_1020_2int():
    try:
        bits2int("1020")
    except AssertionError:
        return
    
    assert False, "Bad bit accepted"
    
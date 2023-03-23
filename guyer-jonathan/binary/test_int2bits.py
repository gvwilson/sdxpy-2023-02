from int2bits import int2bits, bits2int

def test_10_2bits():
    assert int2bits(10) == "1010"

def test_0_2bits():
    assert int2bits(0) == "0"

def test_65535_2bits():
    assert int2bits(65535) == "1111111111111111"

def test_bits2int():
    pass

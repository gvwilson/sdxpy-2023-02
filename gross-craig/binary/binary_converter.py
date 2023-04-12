import sys


def int_to_bits(num):
    """Convert an integer into its binary representation as a string

    Parameters
    ----------
    num : non-negative integer to convert to binary

    Returns
    -------
    String of "0" and "1" bits representing num in binary

    """
    assert num >= 0
    bits = []
    while True:
        bits.append(str(num & 0b1))
        num = num >> 1
        if num == 0:
            break
    return ''.join(reversed(bits))


def bits_to_int(bits):
    """Convert a binary string representation of an integer into a an integer

    Parameters
    ----------
    bits : String of "0"s and "1"s , binary representation of a nonnegative int

    Returns
    -------
    The integer with binary representation bits

    """
    assert len(bits) > 0
    assert bits.count("0") + bits.count("1") == len(bits), "Non-binary string"
    value = [int(bit) * 2 ** place for place, bit in enumerate(reversed(bits))]
    return sum(value)


assert bits_to_int("0") == 0
assert bits_to_int("1") == 1
assert bits_to_int("01") == 1
assert bits_to_int("10") == 2
assert bits_to_int("11") == 3
assert bits_to_int("100") == 4

assert int_to_bits(0) == "0"
assert int_to_bits(1) == "1"
assert int_to_bits(2) == "10"
assert int_to_bits(4) == "100"
assert int_to_bits(5) == "101"


# Test via roundtrips
for num in [0, 1, 2, 3, 127, 128, 129, sys.maxsize, sys.maxsize + 1]:
    assert bits_to_int(int_to_bits(num)) == num, num

for bits in ["1", "10", "101", "111", "1000", "00010"]:
    assert int_to_bits(bits_to_int(bits)) == bits.lstrip("0"), bits

# Can't test by stripping leading zeros
assert int_to_bits(bits_to_int("0")) == "0"

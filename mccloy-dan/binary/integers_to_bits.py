import pytest


def bits_to_int(bitstring):
    # NOTE: bitstring assumed unsigned (result will be strictly nonnegative)
    n_bits = len(bitstring)
    if not n_bits:
        print('zero-length input: undefined behavior')
        return None
    # call to int() will handle non-digit input with a ValueError
    bits = [int(digit) for digit in bitstring]
    nums = [bit * 2 ** i for i, bit in enumerate(reversed(bits))]
    return sum(nums)


def int_to_bits(integer, width=1):
    # NOTE: only works for nonnegative integers.
    assert width > 0, 'minimum width is 1'
    bits = []
    exponent = 0
    while integer >= 2 ** exponent:
        bits.insert(0, int(bool(integer & 2 ** exponent)))
        exponent += 1
    bits = ''.join(map(str, bits))
    bits = f'{bits:0>{width}}'  # left-pad with 0s to `width` if shorter
    return bits


for n in range(23):
    assert n == bits_to_int(int_to_bits(n))

test_cases = (
    '0000',
    '0001',
    '0010',
    '0011',
    '0100',
    '0101',
    '0110',
    '0111',
    '1000',
    '1001',
    '1010',
    '1011',
    '1100',
    '1101',
    '1110',
    '1111',
)

for t in test_cases:
    assert t == int_to_bits(bits_to_int(t), width=4)

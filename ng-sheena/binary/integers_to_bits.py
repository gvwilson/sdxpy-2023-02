from struct import pack

'''
convert non-negative integer into binary representation
'''
def int_to_binary(num:int):
    # ensure that function runs only if it is a non-negative integer
    if num < 0:
        raise ValueError("This function only supports non-negative integer")

    if num == 0:
        return 0

    binary = []
    while num > 0:
        # use AND to extract the least sig bit of num
        bit = num & 1
        binary.insert(0, str(bit))
        # shift right by 1 position to drop the least sig bit of num (halve the value)
        num = num >> 1

    return "".join(binary)

'''
convert binary (string of 1s an 0s) to unsigned integer
'''
def binary_to_int(binary:str):
    decimal = 0

    for bit in binary:
        # shift the decimal 1 position left (double the value)
        # then use OR to set the least sig bit of decimal to current bit in binary
        decimal = (decimal << 1) | int(bit)
    return decimal

TESTS = [3, 40, 482, 590, 1264, 7809]

for test in TESTS:
    assert test == binary_to_int(int_to_binary(test))

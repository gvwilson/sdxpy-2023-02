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
    # while num > 0:
    #     binary.insert(0, str(num % 2))
    #     num //=2

    # print("".join(binary))

    while num > 0:
        bit = num & 1
        binary.insert(0, str(bit))
        num = num >> 1

    return "".join(binary)

'''
convert binary to integer
'''

int_to_binary(42)
int_to_binary(3)

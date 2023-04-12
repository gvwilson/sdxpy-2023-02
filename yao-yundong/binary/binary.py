def if_png(file_path):
    """
        check if the file is PNG image by its first eight bytes.
    """
    
    with open(file_path, "rb") as reader:
        first_eight_bytes = reader.read(8)

    first_eight_values = [i for i in first_eight_bytes]
    head = [137, 80, 78, 71, 13, 10, 26, 10]
    
    return first_eight_values == head

def get_binary_representation(n):
    """
        return the binary representation of a non-negative integer.
    """

    assert isinstance(n, int)
    assert n >= 0

    if n == 0:
        return '0'

    binary = ''
    while n > 0:
        binary = str(n & 1) + binary
        n >>= 1

    return binary

def get_integer_from_binary(binary):
    """
    converts a string of 1's and 0's into an integer.
    """

    assert isinstance(binary, str)

    result = 0
    for bit in binary:
        result <<= 1
        result |= int(bit)

    return result
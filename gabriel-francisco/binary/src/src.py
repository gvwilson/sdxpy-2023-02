def check_png(filename):
    """Check if a file is a PNG file (by checking whether the first 8 bytes are 137 80 78 71 13 10 26 10 in base 10)"""
    with open(filename, 'rb') as f:
        return  f.read(8) == b'\x89PNG\r\n\x1a\n'
    
def convert_integer_to_bits(integer : int):
    """Convert an integer to bits using bitwise operators"""
    bits = []
    while integer > 0:
        bits.append(integer & 1)
        integer >>= 1
    bits.reverse()
    return "".join(str(bit) for bit in bits)

def convert_bits_to_integer(bits : str):
    """Convert bits to an integer using bitwise operators"""
    integer = 0
    for bit in bits:
        integer <<= 1
        integer |= int(bit)
    return integer
def int2bits(integer):
    result = ""
    remainder = integer
    while remainder != 0:
        result = ("1" if (remainder & 1) else "0") + result
            
        remainder >>= 1
        
    if len(result) == 0:
        result = "0"

    return result

def bits2int(bits):
    pass
import re

# Question 2
def int_to_bits(integer):
    """Given a non-negative integer, 
    return its binary representation.
    """
    # check if input is valid
    assert isinstance(integer, int), f"input is not an integer"
    assert integer >= 0, f"input is not a non-negative integer"
    
    bits_list = []
    
    while integer > 0:
        bit = integer & 0b1
        bits_list.append(str(bit)) # coerce to allow for string manipulations
        integer = integer >> 1
    
    if integer == 0:
        bits_list.append('0')
        
    binary_rep = ''.join(bits_list)[::-1] # reverse order of list
    
    return(binary_rep)

def bits_to_int(string):
    """Convert a string of 1's and 0's (unsigned binary number)
    into an integer.
    """
    # check if input is valid
    pattern = "^[01]+$"
    assert bool(re.match(pattern, string)), f"input is not a string of 1's and 0's"
    
    acc = 0

    for i in range(len(string)):
        exp = len(string) - 1 - i
        acc += int(string[i]) * 2 ** exp
        
    return(acc)

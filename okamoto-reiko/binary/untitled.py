# Question 1
def is_file_png(filepath):
    with open(filepath, 'rb') as f:
        header = f.read(8)
    
    bytes_list = []
    
    for h in header:
        bytes_list.append(h)
        
    if bytes_list == [137, 80, 78, 71, 13, 10, 26, 10]:
        print("file is a PNG image")
    else:
        print("file is not a PNG image")

        
# Question 2
def int_to_bits(integer):
    bits_list = []
    
    while integer > 0:
        bit = integer & 0b1
        bits_list.append(str(bit)) # coerce to allow for string manipulations
        integer = integer >> 1
    
    if integer == 0:
        bits_list.append('0')
        
    binary_rep = ''.join(bits_list)[::-1] # reverse order of list
    
    return(binary_rep)

# Question 3
def bits_to_int(string):
    acc = 0

    for i in range(len(string)):
        exp = len(string) - 1 - i
        acc += int(string[i]) * 2 ** exp
        
    return(acc)
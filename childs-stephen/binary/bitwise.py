# Using Python's bitwise operators,
# write a function that returns the binary representation of a non-negative integer.

input = 9
print(bin(input))

output = ""

while input > 0:
    last_bit = input & 0b1
    output = str(last_bit) + output
    input = input >> 1
print(output)


# Write another function that converts a string of 1's and 0's into an integer
# (treating it as unsigned).

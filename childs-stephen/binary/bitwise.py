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

input2 = "100101"
print(0b100101)

# bin just gives the binary REPRESENTAITON, still stored as an integer.
print(f"first character as integer: {int(input2[0])}")
print(f"first character as binary: {bin(int(input2[0]))}")

output2 = 0b0

# we don't actually need to do it in reverse
for c in reversed(input2):
    print(c)

# we set the last bit using or
for c in input2:
    i = int(c)
    # we do the shift first -- for the first bit the output is already zero
    output2 = output2 << 1
    output2 = output2 | i

print(output2)

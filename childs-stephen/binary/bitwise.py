# Using Python's bitwise operators,
# write a function that returns the binary representation of a non-negative integer.

input = 9
print(bin(input))


def to_binary(input):
    output = ""

    while input > 0:
        last_bit = input & 0b1
        output = str(last_bit) + output
        input = input >> 1
    return output


# Write another function that converts a string of 1's and 0's into an integer
# (treating it as unsigned).

input2 = "100101"
print(0b100101)

# bin just gives the binary REPRESENTAITON, still stored as an integer.
print(f"first character as integer: {int(input2[0])}")
print(f"first character as binary: {bin(int(input2[0]))}")


# we don't actually need to do it in reverse
for c in reversed(input2):
    print(c)


# we set the last bit using or
def to_integer(input):
    output = 0b0
    for c in input:
        i = int(c)
        # we do the shift first -- for the first bit the output is already zero
        output = output << 1
        output = output | i
    return output


def roundtrip1(integer):
    return integer == to_integer(to_binary(integer))


def roundtrip2(string):
    return string == to_binary(to_integer(string))


TESTS = [0, 8, 9, 100, 1001, 998, 9989]

for i in TESTS:
    print(f"integer: {i}\tbinary:{to_binary(i)}")
    assert roundtrip1(i)

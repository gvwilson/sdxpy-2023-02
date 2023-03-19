# Using Python's bitwise operators,
# write a function that returns the binary representation of a non-negative integer.


def to_binary(input):
    output = ""

    if input == 0:
        return "0b0"

    while input > 0:
        last_bit = input & 0b1
        output = str(last_bit) + output
        input = input >> 1
    return "0b" + output


# Write another function that converts a string of 1's and 0's into an integer
# (treating it as unsigned).


# we set the last bit using or
def to_integer(input):
    if input[0:2] == "0b":
        input = input[2:]
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


sixty_four = to_integer("0b1" + 63 * "0")
one_twenty_eight = to_integer("0b1" + 127 * "0")

print(sixty_four)
print(one_twenty_eight)


TESTS = [0, 8, 9, 100, 1001, 998, 9989, 2147483647, sixty_four, one_twenty_eight]

print("Decimal (represented as integer) roundtrip")
for i in TESTS:
    print(f"decimal: {i}\nbinary:{to_binary(i)}\n")
    assert to_binary(i) == bin(i)
    assert roundtrip1(i)

print("Binary (represented as string) roundtrip")
for i in TESTS:
    str_i = bin(i)
    print(f"binary: {str_i}\ndecimal:{to_integer(str_i)}\n")
    assert roundtrip2(str_i)

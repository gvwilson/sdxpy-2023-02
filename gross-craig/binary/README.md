## File Types

The first eight bytes of a PNG image file always contain the following (base-10) values:

```
137 80 78 71 13 10 26 10
```

Write a program that determines whether a file is a PNG image or not.

### Solution

This is implemented in `is_png.py` by loading the file for binary reading and
checking equality of this header with the first eight bytes. I've added three
small test files `test_header.png`, `test_image.png`, and `test.txt` to test the
function.

## Converting Integers to Bits

Using Python's bitwise operators,
write a function that returns the binary representation of a non-negative integer.
Write another function that converts a string of 1's and 0's into an integer
(treating it as unsigned).

### Solution

This is implemented in `binary_converter.py`.

To convert an integer to its bit representation in `ints_to_bits`, the integer
is masked  with the bit `0b1` to get its first bit, then right shifted. The
process is repeated so all bits are recorded until the number zeros out.

To convert a bit string to an integer, the bits are used as coefficients of
powers of 2, assembled using a list comprehension over an `enumerate` of the bit
string. These values are summed to produce the final value.
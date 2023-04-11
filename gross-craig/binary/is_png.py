import argparse


def is_png(filename):
    """Check whether the given file is a png

    Parameters
    ----------
    filename : Filename to check

    Returns
    -------
    True if png, False otherwise

    """
    with open(filename, "rb") as file:
        header = file.read(8)
    return header == bytes([137, 80, 78, 71, 13, 10, 26, 10])


assert is_png("test_header.png")
assert is_png("test_image.png")
assert not is_png("test.txt")

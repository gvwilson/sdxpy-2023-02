import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import check_png, convert_integer_to_bits, convert_bits_to_integer

def test_check_png():
    """Loop through all PNG files in the png directory and confirm if all are PNG files"""
    png_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "png"))
    for filename in os.listdir(png_dir):
        path = os.path.join(png_dir, filename)
        assert check_png(path) == True

def test_non_png():
    """Loop through the non-png directory and confirm files are not a identified as PNG files"""
    non_png_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "non-png"))
    for filename in os.listdir(non_png_dir):
        path = os.path.join(non_png_dir, filename)
        assert check_png(path) == False

def test_convert_int_to_bit():
    """Test the convert_integer_to_bits function"""
    inputs = [1,2,54,31,982,12154,1024    ] # 0 is actually a problem
    for i in inputs:
        assert convert_integer_to_bits(i) == bin(i)[2:]

def test_convert_bit_to_int():
    """Test the convert_bits_to_integer function"""
    inputs = [1,2,54,31,982,12154,1024    ] # 0 is actually a problem
    for i in inputs:
        assert convert_bits_to_integer(bin(i)[2:]) == i

def test_round_trip():
    """Test the round trip of converting an integer to bits and back to an integer"""
    inputs = [1,2,54,31,982,12154,1024    ] # 0 is actually a problem
    for i in inputs:
        assert convert_bits_to_integer(convert_integer_to_bits(i)) == i
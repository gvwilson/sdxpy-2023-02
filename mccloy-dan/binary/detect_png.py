import sys

magic = [137, 80, 78, 71, 13, 10, 26, 10]

files = sys.argv[1:]

for file in files:
    with open(file, 'rb') as ff:
        bytes_read = ff.read(len(magic))
    is_png = (bytes_read == bytes(magic))
    neg = '' if is_png else ' not'
    print(f'{file} is{neg} a PNG file.')

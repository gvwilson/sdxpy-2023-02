png_bytes = (137, 80, 78, 71, 13, 10, 26, 10)

def is_png(filePath):
    with open(filePath, 'rb') as file:
        first_eight_bytes = file.read(8)
        print(first_eight_bytes)

        if first_eight_bytes == bytes(png_bytes):
            return True

        return False

print(is_png('test1.txt'))
print(is_png('empty.png'))
print(is_png('koala.png'))

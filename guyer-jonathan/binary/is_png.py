import sys

PNG_magic = [137, 80, 78, 71, 13, 10, 26, 10]

def is_png(path):
    with open(path, mode='rb') as f:
        result = True
        for magic_char in PNG_magic:
            char = f.read(1)
            result &= (ord(char) == magic_char)
        
    return result

if __name__ == "__main__":
    assert len(sys.argv) == 2, f"Expected file path, got {sys.argv}"
    print(int(is_png(sys.argv[1])))

import sys

png_bytes = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a"


def is_png(content):
    return content[:8] == png_bytes


def png_check_file(filename):
    with open(filename, "rb") as f:
        contents = f.read()
        return is_png(contents)


assert png_check_file("python-logo-only.png"), "false negative"
assert png_check_file("README.md") == False, "false positive"

files = sys.argv[1:]

for f in files:
    print(f"{f}...{png_check_file(f)}")

# The first eight bytes of a PNG image file always contain the following (base-10) values:
# 137 80 78 71 13 10 26 10
# Write a program that determines whether a file is a PNG image or not.

decimal_bytes = [137, 80, 78, 71, 13, 10, 26, 10]
hex_bytes = [hex(i) for i in decimal_bytes]
print(hex_bytes)

png_bytes = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a"

with open("ZoomBG_Winter4.png", "rb") as f:
    contents = f.read()
    print(contents[:8])
    if contents[:8] == png_bytes:
        print("PNG file detected")

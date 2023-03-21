# Special thanks to Google, since I thought I was going to have to use struct().
def png_detect(filename = r"C:\Users\Fraser\Desktop\Homework\manifestb - Copy.csv"):
    png_signature = [137, 80, 78, 71, 13, 10, 26, 10] # PNG signature
    with open(filename, 'rb') as f: # Binary mode
        header = f.read(8) # First 8 bytes of the file
    if list(header) == png_signature: # Compare with the expected header
        print("PNG detected!")
    else:
        print("No PNG for you.")

# Question 1

import sys

def is_file_png(filepath):
    """Given a file path, determine whether the file is a PNG.
    """
    with open(filepath, 'rb') as f:
        header = f.read(8)
    
    bytes_list = []
    
    for h in header:
        bytes_list.append(h)
        
    if bytes_list == [137, 80, 78, 71, 13, 10, 26, 10]:
        print("=>file is a PNG image")
    else:
        print("=>file is not a PNG image")
        
def main():
    is_file_png(sys.argv[1])
    
if __name__ == "__main__":
    main()

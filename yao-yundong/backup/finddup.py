from collections import defaultdict
import hashlib
import sys


BUFFER_SIZE = 4 * 1024  # how much data to read at once

def hash_stream(reader):
    sha256 = hashlib.sha256()
    while True:
        block = reader.read(BUFFER_SIZE)
        if not block:
            break
        sha256.update(block)
    return sha256.hexdigest()



def find_dup(files_lst):
    results = defaultdict(list)
    for file in files_lst:
        with open(file, "rb") as reader:
            hash_code = hash_stream(reader)
            results[hash_code].append(file)
    return list(results.values())

def main():
    assert len(sys.argv) == 2, "Usage: filedup.py file_name"

    result = find_dup(sys.argv[1])
    for r in result:
        print(r)

if __name__ == "__main__":
    main()

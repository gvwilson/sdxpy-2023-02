import hashlib
import sys

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

def finddup(filenames):
    result = []
    for filename in filenames:
        with open(filename, "rb") as reader:
            hash_code = hash_stream(reader)
            result.append((filename, hash_code))

    duplicates = {}
    for filename, hash_code in result:
        if hash_code in duplicates:
            duplicates[hash_code].append(filename)
        else:
            duplicates[hash_code] = [filename]

    return duplicates

def reportdup(duplicates):
    for hash_code, filenames in duplicates.items():
        if len(filenames) > 1:
            print(f"{filenames} are duplicates")

if __name__ == "__main__":
    # python finddup.py test/files/fileA.txt test/files/fileB.txt test/files/fileD.txt test/files/folder/fileC.txt test/files/folder/fileE.txt
    filenames = sys.argv[1:]
    reportdup(finddup(filenames))

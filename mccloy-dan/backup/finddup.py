import hashlib
import sys

from collections import defaultdict

BUFFER_SIZE = 4 * 1024  # how much data to read at once


def hash_stream(reader):
    sha256 = hashlib.sha256()
    while True:
        block = reader.read(BUFFER_SIZE)
        if not block:
            break
        sha256.update(block)
    return sha256.hexdigest()


def find_duplicates(fnames):
    results = defaultdict(list)
    for fname in fnames:
        with open(fname, "rb") as reader:
            checksum = hash_stream(reader)
            results[checksum].append(fname)
    return results


if __name__ == "__main__":
    fnames = sys.argv[1:]
    results = find_duplicates(fnames)
    for checksum, fnames in results.items():
        if len(fnames) == 1:
            print(f"file {fnames[0]} is unique")
        else:
            print(f"files {', '.join(fnames)} are identical")

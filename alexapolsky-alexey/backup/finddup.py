import sys
from hash_stream import hash_stream


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


if __name__ == "__main__":
    print("Finding dupes.")
    filenames = sys.argv[1:]
    res = finddup(filenames)
    for hash_code, filenames in res.items():
        if len(filenames) > 1:
            print(f"{filenames} are duplicates")

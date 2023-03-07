import hashlib
from glob import glob
from pathlib import Path

BUFFER_SIZE = 4 * 1024


def hash_stream(reader):
    sha256 = hashlib.sha256()
    while True:
        block = reader.read(BUFFER_SIZE)
        if not block:
            break
        sha256.update(block)
    return sha256.hexdigest()


def hash_all(root):
    result = []
    for filename in glob("**/*.txt", root_dir=root, recursive=True):
        full_name = Path(root, filename)
        with open(full_name, "rb") as reader:
            hash_code = hash_stream(reader)
            result.append((filename, hash_code))
    return result


if __name__ == "__main__":
    print(hash_all("test/"))

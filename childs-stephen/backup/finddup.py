import hashlib
from glob import glob
from pathlib import Path
from collections import defaultdict

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


def group_files(hash_list):
    result = defaultdict(list)
    for f, h in hash_list:
        result[h].append(f)
    return result


def print_groups(dupe_dict):
    groups = [(v) for k, v in dupe_dict.items()]
    return [i for i in groups if len(i) > 1]


if __name__ == "__main__":
    print(print_groups(group_files(hash_all("test/"))))

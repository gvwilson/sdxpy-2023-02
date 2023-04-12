import argparse
from pathlib import Path
import hashlib

# set up argparse to take in file name as command line arg
parser = argparse.ArgumentParser()
parser.add_argument("file_name")
args = parser.parse_args()

target_file = args.file_name

# create hash
def hash_stream(reader):
    BUFFER_SIZE = 4 * 1024
    sha256 = hashlib.sha256()
    while True:
        block = reader.read(BUFFER_SIZE)
        if not block:
            break
        sha256.update(block)
    return sha256.hexdigest()

# read target file and create hash for target file
target_reader = open(target_file, "rb")
target_hash = hash_stream(target_reader)

# read files in all directories
all_entries = list(Path().rglob("*"))

# find duplicate files
duplicates = []
for entry in all_entries:
    if entry.is_file():
        file_reader = open(entry, "rb")
        file_hash = hash_stream(file_reader)
        if file_hash == target_hash:
            duplicates.append(entry.name)

# remove target file in duplicates list
duplicates.remove(Path(target_file).name)
print(f"duplicated files found: ", duplicates)

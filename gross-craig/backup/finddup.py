import argparse
from pathlib import Path
import logging
import hashlib


BUFFER_SIZE = 4 * 1024


def hash_sha256(file_path):
    """Hash an existing file with a sha256 hash

    Parameters
    ----------
    file_path: Path to file to hash

    Returns
    -------
    sha256 digest of file

    """
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while True:
            block = file.read(BUFFER_SIZE)
            if not block:
                break
            sha256.update(block)
    return sha256.hexdigest()


def group_hashes(hashes):
    """Group files by their hashes

    Parameters
    ----------
    hashes : A dictionary with file paths as keys and hashes as values

    Returns
    -------
    A dictionary with hashes as keys and value of a list of file paths with
    those hashes sorted by filename

    """
    groups = {hash_val: [] for hash_val in set(hashes.values())}
    for file, hash_val in hashes.items():
        groups[hash_val].append(file)
    for files in groups.values():
        files.sort(key=lambda file: file.name)
    return groups


def print_groups(groups):
    """Print files grouped by hashes

    Parameters
    ----------
    groups : A dictionary with hashes as keys and files with those hashes as
        values

    Returns
    -------
    None

    """
    for file_paths in sorted(groups.values()):
        files = [path.name for path in file_paths]
        print("duplicates:\n\t" + '\n\t'.join(files))


def main(*files):
    """TODO:

    Parameters
    ----------
    files : Filenames to compare for duplicates

    Returns
    -------
    A dictionary with hashes as keys and value of a list of file paths with
    those hashes sorted by filename (see group_hashes for more information)

    """
    paths = [Path(file) for file in files]
    for file in paths:
        if not file.exists():
            logging.warning(f"File {file} does not exist")
    hashes = {file: hash_sha256(file) for file in paths if file.exists()}
    groups = group_hashes(hashes)
    print_groups(groups)
    return groups


if __name__ == "__main__":
    USAGE = "Finds all groups of duplicate files"
    parser = argparse.ArgumentParser(description=USAGE)
    parser.add_argument("file", type=str, nargs="+", help="File name")
    args = parser.parse_args()
    main(*args.file)

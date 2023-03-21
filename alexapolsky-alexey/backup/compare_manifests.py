import csv
import shutil
import time
from pathlib import Path
from hash_all import hash_all
from manifest_functions import read_manifest, read_manifests
from pprint import pprint


def current_time():
    return f"{time.time()}".split(".")[0]


def write_manifest(backup_dir, timestamp, manifest):
    backup_dir = Path(backup_dir)
    if not backup_dir.exists():
        backup_dir.mkdir()
    manifest_file = Path(backup_dir, f"{timestamp}.csv")
    with open(manifest_file, "w") as raw:
        writer = csv.writer(raw)
        writer.writerow(["filename", "hash"])
        writer.writerows(manifest)


def copy_files(source_dir, backup_dir, manifest):
    for (filename, hash_code) in manifest:
        source_path = Path(source_dir, filename)
        backup_path = Path(backup_dir, f"{hash_code}.bck")
        if not backup_path.exists():
            shutil.copy(source_path, backup_path)


def backup(source_dir, backup_dir):
    manifest = hash_all(source_dir)
    timestamp = current_time()
    write_manifest(backup_dir, timestamp, manifest)
    copy_files(source_dir, backup_dir, manifest)
    return manifest


def compare_manifests(manifests):
    # manifests = manifests[start_index:start_index+2]

    result = {}

    file_states = {}
    file_states2 = {}

    for (filename, hash) in manifests[0]:
        file_states[filename] = hash

    for (filename, hash) in manifests[1]:
        file_states2[filename] = hash

    reversed_hashes_old = {}
    for k, v in file_states.items():
        reversed_hashes_old[v] = k

    reversed_hashes2 = {}
    for k, v in file_states2.items():
        reversed_hashes2[v] = k

    renamed_hashes = []

    for (filename, hash) in manifests[1]:

        if filename not in file_states.keys() and not hash in reversed_hashes_old:
            result[filename] = f"{filename} file contents has been added"

        if filename in file_states and file_states[filename] != hash:
            result[filename] = f"{filename} file contents has changed"

        if hash in reversed_hashes_old and filename != reversed_hashes_old[hash]:
            renamed_hashes.append(hash)
            result[filename] = f"{filename} file has been renamed"

    missing_hashes = sorted(
        set(file_states.values()) - set(file_states2.values()) - set(renamed_hashes)
    )
    for hash in missing_hashes:
        filename = reversed_hashes_old[hash]
        if filename not in file_states2.keys():  # wasn't a content change
            result[filename] = f"{filename} file has been deleted"

    return result


if __name__ == "__main__":
    manifests = read_manifests("backup_dir")
    res = compare_manifests(manifests)
    pprint(res)

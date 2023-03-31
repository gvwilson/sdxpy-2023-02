import csv
from pathlib import Path


RESULT_TEMPLATE = {
    "same":
        lambda file: f"{file}: unchanged",
    "changed":
        lambda file: f"{file}: changed",
    "renamed":
        lambda files: f"{files[0]}: renamed to {files[1]}",
    "deleted":
        lambda file: f"{file}: deleted",
    "added":
        lambda file: f"{file}: added",
}


def read_manifest(manifest_path):
    """Read a manifest written as a csv into a dictionary.
    The manifest is assumed to be a csv in the form:

    filename,hash
    a.txt,abc123
    b.txt,def456

    and so on.


    Parameters
    ----------
    manifest_path : Filename of existing manifest

    Returns
    -------
    A dictionary with filenames as keys and hashes as values

    """
    with open(manifest_path, newline='') as manifest_file:
        reader = csv.DictReader(manifest_file)
        manifest_dict = {row["filename"]: row["hash"] for row in reader}
    return manifest_dict


def join_manifests(*manifests):
    """Outer join dictionaries representing manifests

    Parameters
    ----------
    manifests: Dictionaries with filenames as keys pointing to hash values

    Returns
    -------
    A dictionary with all filenames as keys pointing to a list of
    length len(manifests). Each item is the hash from the corresponding
    manifest. If the hash does not exist for that manifest, the value is
    none.

    """
    all_files = {}
    for manifest in manifests:
        all_files = {*all_files, *manifest.keys()}
    comparison = {}
    for file in all_files:
        file_hashes = [manifest.get(file, None) for manifest in manifests]
        comparison[file] = file_hashes
    return comparison


def find_hash(comparison, hash_val, col=1):
    """Search a comparison dictionary for a specified hash

    Parameters
    ----------
    comparison : A comparison dictionary (see join_manifests for details)
    hash : The hash to search for
    col : The element of each hash list to search

    Returns
    -------
    The filenames matching the hash as a (possibly empty) list

    """
    matches = []
    for file, hashes in comparison.items():
        if hash_val == hashes[col]:
            matches.append(file)
    return matches


def get_manifest_paths(manifest_dir):
    """Return the paths of all manifests in a directory.
    Manifests are .csv files with ten digit filenames representing Unix time
    stamps.

    Parameters
    ----------
    manifest_dir : The directory to search for manifests

    Returns
    -------
    An array containing path objects for all manifests in manifest_dir

    """
    dir_path = Path(manifest_dir)
    assert dir_path.is_dir()
    manifest_pattern = ['[0-9]'] * 10
    manifest_pattern.append('.csv')
    manifest_pattern = ''.join(manifest_pattern)
    return sorted(dir_path.glob(manifest_pattern))

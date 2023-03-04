import csv


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


def join_manifests(curr, prev):
    """Outer join dictionaries representing manifests

    Parameters
    ----------
    curr : A dictionary with filenames as keys pointing to hash values
    prev : Same as curr, but representing previous state of files

    Returns
    -------
    A dictionary with all filenames as keys pointing to a list of length two.
    The first item is the previous hash and the second item is the current
    hash. If either hash does not exist, the value in the list is None

    """
    all_files = {*curr.keys(), *prev.keys()}
    comparison = {file:
                  [prev.get(file, None),
                   curr.get(file, None)] for file in all_files}
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


def parse_comparison(comparison):
    """Convert a dictionary of file and hash comparisons to a report.
    The results are stored as a dictionary where files are sorted by status
    into "same", "changed", "renamed", "deleted", or "added"

    Parameters
    ----------
    comparison : A dictionary containing a comparison of two manifests (see
        join_manifests for more information)

    Returns
    -------
    A dictionary with keys "same", "changed", "renamed", "deleted", or "added"
    with lists as values containing the associated files. The "renamed" value
    is a list of lists, where the first entry of each inner list is the
    original file name, and the second entry is the current file name

    """
    report = {
        "same": [],
        "changed": [],
        "renamed": [],
        "deleted": [],
        "added": []
    }
    rename_targets = []
    for file, hashes in comparison.items():
        old_hash, new_hash = hashes
        if old_hash is None:
            report["added"].append(file)
        elif new_hash is None:
            matches = find_hash(comparison, old_hash)
            if matches:
                rename_targets.append(matches[0])
                report["renamed"].append([file, matches[0]])
            else:
                report["deleted"].append(file)
        elif old_hash == new_hash:
            report["same"].append(file)
        else:  # old_hash != new_hash
            report["changed"].append(file)

    # renames should not be considered added files
    for target in rename_targets:
        if target in report["added"]:
            report["added"].remove(target)
    return report


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


def print_comparison_report(report):
    """Print the results of comparing two manifests

    Parameters
    ----------
    report : A dictionary with statuses pointing to the files with that status
        (see parse_comparison for details)

    Returns
    -------
    None

    """
    print_string = []
    for status in report.keys():
        if status != "same":
            for file in report[status]:
                print_string.append(RESULT_TEMPLATE[status](file))
    print_string.sort()  # display files alphabetically
    print("\n".join(print_string))


def compare_manifests(curr_path, prev_path):
    """Compares two manifests by reporting
    - Which files have had their contents changed
    - Which files have been renamed
    - Which files have been deleted
    - Which files have been added

    Parameters
    ----------
    curr_path: filename of "current" manifest
    prev_path: filename of manifest to compare current manifest against

    Returns
    -------
    A report of file changes between manifests

    """
    curr = read_manifest(curr_path)
    prev = read_manifest(prev_path)
    comparison = join_manifests(curr, prev)
    report = parse_comparison(comparison)
    print_comparison_report(report)
    return report

from manifest_utils import (read_manifest, join_manifests, find_hash,
                            RESULT_TEMPLATE)


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
    comparison = join_manifests(prev, curr)
    report = parse_comparison(comparison)
    print_comparison_report(report)
    return report

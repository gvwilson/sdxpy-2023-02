import csv

def read_manifest(manifest_path):
    """Read a manifest written as a csv into a dictionary.
    The manifest is assumed to be a csv in the form:

    filename,hash
    a.txt,123
    b.txt,456

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
    return comparison
    # report = parse_comparison(comparison)
    # print_report(report)
    # return report


if __name__ == "__main__":
    print(compare_manifests("0000000001.csv", "0000000000.csv"))

def read_manifest_as_dict(fname):
    import csv

    _dict = dict()
    with open(fname, 'r') as ff:
        for line in csv.reader(ff):
            assert len(line) == 2
            _fname, _hash = line
            assert _hash not in _dict
            _dict[_hash] = _fname
    return _dict


def compare_manifests(one, two):
    """Print the differences between two manifests, given their filenames.

    Output shows changes from manifest `one` to `two` (in that order).
    """
    state_one = read_manifest_as_dict(one)
    state_two = read_manifest_as_dict(two)
    output = list()

    for _hash, _fname in state_two.items():
        if _hash in state_one:
            old_fname = state_one[_hash]
            if old_fname == _fname:  # hash same, fname same
                continue
            else:  # hash same, fname different
                output.append(
                    {(old_fname, _fname): f'renamed: {old_fname} -> {_fname}'}
                )
        elif _fname in state_one.values():  # hash different, fname same
            output.append({(_fname,): f'changed: {_fname}'})
        else:  # hash different, fname different (new file)
            output.append({(_fname,): f'created: {_fname}'})

    # need to sort these for stable testing:
    missing_hashes = sorted(set(state_one) - set(state_two))
    for _hash in missing_hashes:
        _fname = state_one[_hash]
        if _fname not in state_two.values():  # wasn't a content change
            output.append({(_fname,): f'deleted: {_fname}'})
    return output


if __name__ == "__main__":
    import sys
    one = sys.argv[1]
    two = sys.argv[2]
    output = compare_manifests(one, two)
    for comparison in output:
        for key, line in comparison.items():
            print(line)

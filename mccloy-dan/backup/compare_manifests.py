import csv


def compare_manifests(one, two):
    """Print the differences between two manifests, given their filenames.

    Output shows changes from manifest `one` to `two` (in that order).
    """
    state_one = dict()
    state_two = dict()
    output = list()

    for _file, _dict in zip([one, two], [state_one, state_two]):
        with open(_file, 'r') as ff:
            for line in csv.reader(ff):
                assert len(line) == 2
                _fname, _hash = line
                assert _hash not in _dict
                _dict[_hash] = _fname

    for _hash, _fname in state_two.items():
        if _hash in state_one:
            old_fname = state_one[_hash]
            if old_fname == _fname:  # hash same, fname same
                continue
            else:  # hash same, fname different
                output.append(f'renamed: {old_fname} -> {_fname}')
        elif _fname in state_one.values():  # hash different, fname same
            output.append(f'changed: {_fname}')
        else:  # hash different, fname different (new file)
            output.append(f'created: {_fname}')

    missing_hashes = set(state_one) - set(state_two)
    for _hash in missing_hashes:
        if state_one[_hash] not in state_two.values():  # wasn't content change
            output.append(f'deleted: {state_one[_hash]}')
    return output


if __name__ == "__main__":
    import sys
    one = sys.argv[1]
    two = sys.argv[2]
    output = compare_manifests(one, two)
    for line in output:
        print(line)

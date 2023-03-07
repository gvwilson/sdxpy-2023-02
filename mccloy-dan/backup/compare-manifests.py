import csv
import sys

one = sys.argv[1]
two = sys.argv[2]

state_one = dict()
state_two = dict()

for _file, _dict in zip([one, two], [state_one, state_two]):
    with open(_file, 'r') as ff:
        for line in csv.reader(ff):
            assert len(line) == 2
            _fname, _hash = line
            assert _hash not in _dict
            _dict[_hash] = _fname


for _hash, _fname in state_two.items():
    old_fname = state_one.get(_hash, None)
    if old_fname == _fname:  # hash same, fname same
        continue
    elif old_fname is not None:  # hash same, fname changed
        print(f'renamed: {old_fname} -> {_fname}')
    elif _fname in state_one.values():  # hash new, fname old (content changed)
        print(f'changed: {_fname}')
    else:  # hash new, fname new (new file)
        print(f'created: {_fname}')

missing_hashes = set(state_one) - set(state_two)
for _hash in missing_hashes:
    if state_one[_hash] not in state_two.values():  # wasn't a content change
        print(f'deleted: {state_one[_hash]}')

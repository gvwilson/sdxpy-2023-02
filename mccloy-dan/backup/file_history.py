import csv
import sys

from collections import ChainMap
from glob import glob
from pathlib import Path


# the filename whose history we want to trace
fname = sys.argv[1]

manifests = sorted(glob("./manifests/*.csv"))

hash_dicts = list()  # where we'll store the manifests
timestamps = list()  # extracted from the filenames
history = list()  # the output messages

# because these are sorted chronologically, we'll get a ChainMap with the
# *oldest* manifest at the "top" / searched first
for manifest in sorted(manifests):
    hash_dict = dict()
    with open(manifest, "r") as ff:
        for line in csv.reader(ff):
            assert len(line) == 2
            _fname, _hash = line
            assert _fname not in hash_dict, "duplicate fnames in one manifest"
            hash_dict[_fname] = _hash
    hash_dicts.append(hash_dict)
    timestamp = Path(manifest).stem.split("-", maxsplit=1)[1]
    timestamps.append(timestamp)

hash_dicts = ChainMap(*hash_dicts)

try:
    current_hash = hash_dicts[fname]
except KeyError as e:
    raise KeyError(f"filename '{fname}' not found in manifests") from e

current_fname = fname

history = list()

# go forwards in time first
attested_earlier = False
for _map, _t in zip(hash_dicts.maps, timestamps):
    # if the filename is found
    if current_fname in _map:
        found_hash = _map[current_fname]
        if found_hash == current_hash:
            if attested_earlier:
                history.append(f"{_t}: unchanged")
            else:
                history.append(f"{_t}: created")
        else:
            history.append(
                f"{_t}: content changed (hash {current_hash} -> {found_hash})")
            current_hash = found_hash
        attested_earlier = True
    # the filename wasn't found, look for a rename
    elif current_hash in _map.values():
        found_fname = [k for k, v in _map.items() if v == current_hash]
        assert len(found_fname) == 1  # should be guaranteed by prior assert
        if attested_earlier:
            history.append(
                f"{_t}: renamed ({current_fname} -> {found_fname[0]})")
        else:
            # we are lazy and don't log pre-history (before a rename) here
            attested_earlier = True
        current_fname = found_fname[0]
    # not a rename, file doesn't exist yet or it was deleted
    elif attested_earlier:
        history.append(f"{_t}: deleted")
        break
    else:
        pass  # don't print entries for file's pre-history

# now go forwards in time, in case the requested filename was changed midway


for step in history:
    print(step)

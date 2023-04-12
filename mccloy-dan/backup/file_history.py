from copy import deepcopy
from glob import glob
from pathlib import Path

# why we need this absurdity is so beyond me
try:
    from compare_manifests import compare_manifests
except ImportError:
    from .compare_manifests import compare_manifests


def parse_entry(entry):
    entry = deepcopy(entry)
    timestamp, record = entry.popitem()
    involved_fnames, event = record[0].popitem()
    return timestamp, involved_fnames, event


def file_history(fname):
    """Trace the history of a file through the manifests."""

    manifests = sorted(Path(p) for p in glob("./manifests/*.csv"))
    history = list()
    fnames = [fname] if isinstance(fname, (str, Path)) else fname

    for older, newer in zip(manifests[:-1], manifests[1:]):
        timestamp = newer.stem.split("-", maxsplit=1)[1]
        comparisons = compare_manifests(older, newer)
        record = list()
        for comparison in comparisons:
            # keys are always tuples: length 2 for renames, 1 otherwise
            assert len(comparison) == 1
            involved_fnames = list(comparison)[0]
            if any(_name in involved_fnames for _name in fnames):
                record.append(comparison)
                fnames = list(involved_fnames)  # keep tracking under new fname
        if len(record):
            entry = {timestamp: record}
            # check if this is our first hit. if it is, and it's a rename,
            # we need to restart, looking for prior names too
            _, involved_fnames, event = parse_entry(entry)
            if not len(history) and event.startswith("rename"):
                return file_history(involved_fnames)
            else:
                history.append(entry)

    if not len(history):
        print(f"filename '{fname}' not found in manifests")
    return history


if __name__ == "__main__":
    import sys
    fname = sys.argv[1]  # the filename whose history we want to trace
    output = file_history(fname)
    for entry in output:
        timestamp, involved_fnames, event = parse_entry(entry)
        event = (event if event.startswith("renamed") else event.split(":")[0])
        print(f"{timestamp}: {event}")

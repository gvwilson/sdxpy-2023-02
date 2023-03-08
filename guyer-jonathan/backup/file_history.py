import glob
from pathlib import Path
import sys
import time

from compare_manifests import compare_manifests

def by_file(status):
    new_status = {}
    
    for filepath, [oldhash, newhash] in status["changed"].items():
        new_status[filepath] = ["changed", oldhash, newhash]
        
    for filehash, filepath in status["unchanged"].items():
        new_status[filepath] = ["unchanged", filehash]
    
    for filehash, [oldpath, newpath] in status["renamed"].items():
        new_status[newpath] = ["renamed", oldpath, filehash]

    for filehash, filepath in status["deleted"].items():
        new_status[filepath] = ["deleted", filehash]
        
    for filehash, filepath in status["added"].items():
        new_status[filepath] = ["added", filehash]
        
    return new_status

def file_history(filename, repodir="test"):
    manifests = glob.glob("*.csv", root_dir=repodir)
    manifests = [None] + sorted(manifests)
    
    assert len(manifests) > 0
    
    log = []
    
    newer = Path(repodir, manifests[-1])
    for manifest in manifests[::-1]:
        if manifest is not None:
            manifest = Path(repodir, manifest)
        status = compare_manifests(manifest, newer)
        
        status = by_file(status)
        
        if filename in status:
            if newer is None:
                timestamp = "prehistory"
            else:
                timestamp = time.ctime(int(newer.stem))
            event = status[filename]
            log.append([timestamp, event])

            if event[0] == "renamed":
                # follow renamed files
                filename = event[1]

        newer = manifest

    return log

def report_history(log):
    for timestamp, event in log:
        if event[0] == "changed":
            message = f"File hash changed to {event[2]}"
        if event[0] == "renamed":
            message = f"File renamed from {event[1]}"
        if event[0] == "deleted":
            message = f"File deleted"
        if event[0] == "added":
            message = f"File added with hash {event[1]}"

        if event[0] != "unchanged":
            print(timestamp, message)

if __name__ == "__main__":
    filename = sys.argv[1]
    report_history(file_history(filename))

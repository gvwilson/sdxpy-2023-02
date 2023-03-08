import csv

def read_manifest(manifest_file=None):
    """
    Read a manifest `.csv` file into a dictionary
    
    Parameters
    ----------
    manifest_file : str
        Path to `.csv` manifest file

    Returns
    ----
    manifest : dict
        File hash keys with file path values
    """
    manifest = {}
    if manifest_file is not None:
        with open(manifest_file, mode="r") as csvfile:
            manifest_reader = csv.reader(csvfile, delimiter=",")
            for filehash, filename in manifest_reader:
                manifest[filehash] = filename

    return manifest

def compare_manifests(fileA, fileB):
    """
    Compare two manifest `.csv` files
    
    Parameters
    ----------
    fileA, fileB : str
        Paths to `.csv` manifest files to compare

    Returns
    ----
    status : dict
        changed : dict
            Files have the same names but different hashes
            (file path keys with list of old and new hashes as values)
        unchanged : dict
            Files have the same hashes and the same names
            (file hash keys with file path as value)
        renamed : dict
            Files have the same hashes but different names
            (file hash keys with list of old and new paths as values)
        deleted : dict
            Files are in the first hash but neither their names nor their hashes are in the second
            (file hash keys with file path as value)
        added : dict
            Files are in the second hash but neither their names nor their hashes are in the first
            (file hash keys with file path as value)
    """
    manifestA = read_manifest(fileA)
    manifestB = read_manifest(fileB)
    reversedA = {}
    reversedB = {}
    
    status = {
        "changed": {},
        "unchanged": {},
        "renamed": {},
        "deleted": {},
        "added": {}
    }
    
    for filehashA, filenameA in manifestA.items():
        if filehashA in manifestB:
            filenameB = manifestB.pop(filehashA)
            if filenameB == filenameA:
                status["unchanged"][filehashA] = filenameA
            else:
                status["renamed"][filehashA] = [filenameA, filenameB]
        else:
            # not found, so set up for reverse lookup
            reversedA[filenameA] = filehashA

    for filehashB, filenameB in manifestB.items():
        if filenameB in reversedA:
            filehashA = reversedA.pop(filenameB)
            status["changed"][filenameB] = [filehashA, filehashB]
        else:
            # not found, so set up for reverse lookup
            reversedB[filenameB] = filehashB
            
    # anything not removed from reversedA must have been deleted
    for filenameA, filehashA in reversedA.items():
        status["deleted"][filehashA] = filenameA
            
    # anything not removed from reversedB must have been added
    for filenameB, filehashB in reversedB.items():
        status["added"][filehashB] = filenameB

    return status

def report_comparison(fileA, fileB):
    status = compare_manifests(fileA, fileB)
    
    if len(status["unchanged"]) > 0:
        print(f"{len(status['unchanged'])} files are unchanged:")
        for filehash, filename in status["unchanged"].items():
            print(f"\t{filehash}: {filename}")
        print()
        
    if len(status["changed"]) > 0:
        print(f"{len(status['changed'])} file contents are changed:")
        for filename, [oldhash, newhash] in status["changed"].items():
            print(f"\t{filename}: {oldhash} -> {newhash}")
        print()

    if len(status["renamed"]) > 0:
        print(f"{len(status['renamed'])} files are renamed:")
        for filehash, [oldname, newname] in status["renamed"].items():
            print(f"\t{filehash}: {oldname} -> {newname}")
        print()
        
    if len(status["deleted"]) > 0:
        print(f"{len(status['deleted'])} files were deleted:")
        for filehash, filename in status["deleted"].items():
            print(f"\t{filehash}: {filename}")
        print()
        
    if len(status["added"]) > 0:
        print(f"{len(status['added'])} files were added:")
        for filehash, filename in status["added"].items():
            print(f"\t{filehash}: {filename}")
        print()

def test_read():
    manifest = read_manifest("test/123456789.csv")

    expected = {
        'deadbeef': 'path/to/t-bone.txt',
        'cafeb0ba': 'path/to/boba/are_gross.txt',
        'decafbad': 'path/to/caffeine.py',
        '8badf00d': 'path/to/do/not/feel/good.py',
        'deadc0de': 'path/to/do/not/use.py'
    }

    assert manifest == expected

def test_compare():
    status = compare_manifests("test/123456789.csv", "test/1234567890.csv")
    
    expected = {
        "changed": {"path/to/caffeine.py": ["decafbad", "c0ffeeee"]},
        "unchanged": {"deadc0de": "path/to/do/not/use.py"},
        "renamed": {"deadbeef": ["path/to/t-bone.txt", "path/to/porterhouse.txt"],
                    "cafeb0ba": ["path/to/boba/are_gross.txt", "path/to/boba/are_yum.txt"]},
        "deleted": {"8badf00d": "path/to/do/not/feel/good.py"},
        "added": {"bbadbeef": "path/to/smells/bad.csv"}
    }

    assert status == expected

def run_tests():
    skipped = []
    passed = []
    failed = []
    errored = []

    for (name, test) in globals().items():
        if not name.startswith("test_"):
            continue
        if hasattr(test, "skip"):
            print(f"skip: {name}")
            skipped.append(name)
            continue
        try:
            test()
            print(f"pass: {name}")
            passed.append(name)
        except AssertionError as e:
            print("docstring:", test.__doc__)
            if test.__doc__ == "test:assert":
                print(f"pass: {name}")
                passed.append(name)
            elif hasattr(test, "fail"):
                print(f"pass (expected failure): {name}")
                passed.append(name)
            else:
                print(f"fail: {name} {str(e)}")
                failed.append(name)
        except Exception as e:
            print(f"error: {name} {str(e)}")
            errored.append(name)

    print(f"{len(skipped)} tests skipped: {skipped}")
    print(f"{len(passed)} tests passed: {passed}")
    print(f"{len(failed)} tests failed: {failed}")
    print(f"{len(errored)} tests errored: {errored}")

    return skipped, passed, failed, errored

if __name__ == "__main__":
    run_tests()
    
    report_comparison("test/123456789.csv", "test/1234567890.csv")

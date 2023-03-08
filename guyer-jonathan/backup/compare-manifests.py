import csv

def read_manifest(manifest_file):
    manifest = {}
    with open(manifest_file, mode="r") as csvfile:
        manifest_reader = csv.reader(csvfile, delimiter=",")
        for filehash, filename in manifest_reader:
            manifest[filehash] = filename

    return manifest

def compare_manifests(fileA, fileB):
    pass

def test_read():
    manifest = read_manifest("test/manifestA.csv")

    expected = {
        'deadbeef': 'path/to/t-bone.txt',
        'cafeb0ba': 'path/to/boba/are_gross.txt',
        'decafbad': 'path/to/caffeine.py',
        '8badf00d': 'path/to/do/not/feel/good.py',
        'deadc0de': 'path/to/do/not/use.py'
    }

    assert manifest == expected

def test_compare():
    status = compare_manifests("test/manifestA.csv", "test/manifestB.csv")
    
    expected = {
        "changed": [["path/to/caffeine.py", "decafbad", "c0ffeeee"]],
        "unchanged": [["deadc0de", "path/to/do/not/use.py"]],
        "renamed": [["deadbeef", "path/to/t-bone.txt", "path/to/porterhouse.txt"],
                    ["cafeb0ba", "path/to/boba/are_gross.txt", "path/to/boba/are_yum.txt"]],
        "deleted": [["8badf00d", "path/to/do/not/feel/good.py"]],
        "added": [["bbadbeef", "path/to/smells/bad.csv"]]
    }

    assert status == expected

if __name__ == "__main__":
    test_read()
    test_compare()

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

if __name__ == "__main__":
    # compare_manifests(fileA, fileB)
    manifestA = read_manifest("test/manifestA.csv")
    print(manifestA)
    manifestB = read_manifest("test/manifestB.csv")
    print(manifestB)

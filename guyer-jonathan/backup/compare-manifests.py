import csv

def read_manifest(manifestfile):
    manifest = {}
    with open(manifest_file, mode="r") as csvfile:
        manifest_reader = csv.reader(csvfile, delimiter=",")
        for filehash, filename in manifest_reader:
            manifest[filehash] = filename
        
def compare_manifests(fileA, fileB):
    pass

if __name__ == "__main__":
    compare_manifests(fileA, fileB)

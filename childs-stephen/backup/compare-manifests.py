from pathlib import Path
from csv import reader

manifests = [
    Path("test", "0305.csv"),
    Path("test", "0306.csv"),
    Path("test", "0307.csv"),
]


def read_manifest(path):
    contents = {}
    with open(path, "r") as f:
        manifest_reader = reader(f, delimiter=",")
        for row in manifest_reader:
            contents[row[0]] = row[1]
    return contents


if __name__ == "__main__":
    print(read_manifest(manifests[0]))

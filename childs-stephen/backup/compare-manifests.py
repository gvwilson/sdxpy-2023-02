from pathlib import Path
from csv import reader

manifests = [
    Path("test", "0305.csv"),
    Path("test", "0306.csv"),
    Path("test", "0307.csv"),
    Path("test", "0308.csv"),
]


def read_manifest(path):
    contents = {}
    with open(path, "r") as f:
        manifest_reader = reader(f, delimiter=",")
        for row in manifest_reader:
            contents[row[0]] = row[1]
    return contents


def read_all_manifests(manifest_list):
    return [read_manifest(p) for p in manifest_list]


def contents_changed(old, new):
    result = []
    for i in old.keys():
        new_contents = new.get(i, None)
        if new_contents and old[i] != new_contents:
            result.append(i)
    return result


if __name__ == "__main__":
    manifest_data = read_all_manifests(manifests)
    print(manifest_data[2])
    print(manifest_data[3])
    print(f"Contents Changed: {contents_changed(manifest_data[2], manifest_data[3])}")

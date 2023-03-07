from pathlib import Path
from csv import reader
import sys

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


def file_history(manifest_data, filename):
    result = []
    current_filename = filename
    num_manifiests = len(manifest_data)
    last_index = num_manifiests - 1
    stop_early = False
    for i in range(last_index, 0, -1):
        if current_filename in manifest_data[i].keys():
            # in previous state
            new_content = manifest_data[i][current_filename]
            if current_filename in manifest_data[i - 1].keys():
                # contents changed
                old_content = manifest_data[i - 1][current_filename]
                if old_content != new_content:
                    result.append(
                        {
                            "index": i,
                            "event": "contents changed",
                            "old": old_content,
                            "new": new_content,
                        }
                    )
            else:
                old_manifest = manifest_data[i - 1]
                try:
                    found = list(old_manifest.keys())[
                        list(old_manifest.values()).index(new_content)
                    ]
                except ValueError:
                    found = False
                if not found:
                    result.append(
                        {
                            "index": i,
                            "event": "added",
                            "old": "",
                            "new": current_filename,
                        }
                    )
                    # stop checking history
                    if i > 1:
                        stop_early = True
                    break
                elif found != current_filename:
                    result.append(
                        {
                            "index": i,
                            "event": "rename",
                            "old": found,
                            "new": current_filename,
                        }
                    )
                    current_filename = found
                else:
                    # no change
                    pass
        else:
            # file not in current state
            # stop_early = True
            continue
    if not stop_early:
        if current_filename in manifest_data[0].keys():
            result.append(
                {"index": 0, "event": "added", "old": "", "new": current_filename}
            )
    return result


if __name__ == "__main__":
    manifest_data = read_all_manifests(manifests)
    # print("File history new.txt")
    # print(file_history(manifest_data, "new.txt"))
    # print("File history top.txt")
    # print(file_history(manifest_data, "top.txt"))
    # print("File history renamed.txt")
    # print(file_history(manifest_data, "renamed.txt"))
    file = sys.argv[1]
    print(file_history(manifest_data, file))

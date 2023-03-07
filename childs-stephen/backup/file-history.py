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

def file_history(manifest_data, filename):
    result = []
    current_filename = filename
    num_manifiests = len(manifest_data)
    last_index = num_manifiests -1
    for i in range(last_index, 1, -1):
        if current_filename in manifest_data[i].keys():
            #contents changed
            old_content = manifest_data[i - 1][current_filename] 
            new_content = manifest_data[i][current_filename]
            if old_content != new_content:
                result.append({"event": "contents changed", "old": old_content, "new": new_content})
            else:
                old_manifest = manifest_data[i - 1]
                found = list(old_manifest.keys())[list(old_manifest.values()).index(new_content)]
                if not found:
                    result.append("event": "added", "old": "", "new": current_filename)
                    #stop checking history
                    break
                elif found != current_filename:
                    result.append({"event": "rename", "old": found, "new": current_filename})
                    current_filename = found
                else:
                    #no change
                    pass 
        else:
            # file not in current state
            break
    return result


if __name__ == "__main__":
    manifest_data = read_all_manifests(manifests)
    print(file_history(manifest_data, "new.txt"))
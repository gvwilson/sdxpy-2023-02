import csv
from collections import defaultdict

manifests = {
    "manifest1.csv": {},
    "manifest2.csv": {}
}

def read_manifest(manifest, my_dict):
    with open(f'{manifest}', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            file_name = row[0]
            hash = row[1]
            my_dict[file_name] = hash
    return my_dict

# Which files have the same names but different hashes
# (i.e., their contents have changed).
def show_hash_change(manifests):
    hash_change_map = defaultdict(list)
    for manifest in manifests.values():
        for file_name, hash_value in manifest.items():
            hash_change_map[file_name].append(hash_value)

    files_hash_changed = []
    for file_name, hash_value in hash_change_map.items():
        if len(hash_value) >= 2:
            files_hash_changed.append(file_name)

    print("file content changed: \n", files_hash_changed)

# Which files have the same hashes but different names
# (i.e., they have been renamed).
def show_file_name_change(manifests):
    name_change_map = defaultdict(list)
    for manifest in manifests.values():
        for file_name, hash_value in manifest.items():
            name_change_map[hash_value].append(file_name)

    file_name_changed = []
    for hash_value, file_name in name_change_map.items():
        if len(file_name) >= 2:
            file_name_changed.append(file_name)

    print("file name changed: \n", file_name_changed)

# Which files are in the first hash but neither their names nor their hashes are in the second
# (i.e., they have been deleted).
def show_file_deleted(manifests):
    file_deletion_list = list()
    manifest1 = manifests[(list(manifests.keys())[0])]
    manifest2 = manifests[(list(manifests.keys())[1])]
    for file_name, hash_value in manifest1.items():
        if file_name not in manifest2 and hash_value not in manifest2.values():
            file_deletion_list.append(file_name)

    print("files deleted: \n", file_deletion_list)

# Which files are in the second hash but neither their names nor their hashes are in the first
# (i.e., they have been added).
def show_file_added(manifests):
    new_file_list = list()
    manifest1 = manifests[(list(manifests.keys())[0])]
    manifest2 = manifests[(list(manifests.keys())[1])]
    for file_name, hash_value in manifest2.items():
        if file_name not in manifest1 and hash_value not in manifest1.values():
            new_file_list.append(file_name)

    print("files added: \n", new_file_list)

def main():
    for my_manifest, my_dict in manifests.items():
        my_dict = read_manifest(my_manifest, my_dict)
        manifests[my_manifest] = my_dict

    show_hash_change(manifests)
    show_file_name_change(manifests)
    show_file_deleted(manifests)
    show_file_added(manifests)

if __name__ == "__main__":
    main()


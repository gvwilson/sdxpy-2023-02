import csv
from collections import defaultdict

manifests = {
    "manifest1.csv": {},
    "manifest2.csv": {}
}

# read the manifest and write data into the dictionary
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
    hash_change_dict = defaultdict(list)
    for manifest in manifests.values():
        for file_name, hash_value in manifest.items():
            hash_change_dict[file_name].append(hash_value)

    hash_changed_files = []
    for file_name, hash_value in hash_change_dict.items():
        if len(hash_value) >= 2:
            hash_changed_files.append(file_name)

    return hash_changed_files

# Which files have the same hashes but different names
# (i.e., they have been renamed).
def show_file_name_change(manifests):
    name_change_dict = defaultdict(list)
    for manifest in manifests.values():
        for file_name, hash_value in manifest.items():
            name_change_dict[hash_value].append(file_name)

    name_changed_files = []
    for hash_value, file_name in name_change_dict.items():
        if len(file_name) >= 2:
            name_changed_files.extend(file_name)

    return name_changed_files

# Which files are in the first hash but neither their names nor their hashes are in the second
# (i.e., they have been deleted).
def show_file_deleted(manifests):
    file_deletion_list = list()
    manifest1 = manifests[(list(manifests.keys())[0])]
    manifest2 = manifests[(list(manifests.keys())[1])]
    for file_name, hash_value in manifest1.items():
        if file_name not in manifest2 and hash_value not in manifest2.values():
            file_deletion_list.append(file_name)

    return file_deletion_list

# Which files are in the second hash but neither their names nor their hashes are in the first
# (i.e., they have been added).
def show_file_added(manifests):
    new_file_list = list()
    manifest1 = manifests[(list(manifests.keys())[0])]
    manifest2 = manifests[(list(manifests.keys())[1])]
    for file_name, hash_value in manifest2.items():
        if file_name not in manifest1 and hash_value not in manifest1.values():
            new_file_list.append(file_name)

    return new_file_list

def populate_manifest():
    for my_manifest, my_dict in manifests.items():
        my_dict = read_manifest(my_manifest, my_dict)
        manifests[my_manifest] = my_dict
    return manifests

def main():
    manifests = populate_manifest()

    print("file content changed: \n", show_hash_change(manifests))
    print("file name changed: \n", show_file_name_change(manifests))
    print("files added: \n", show_file_added(manifests))
    print("files deleted: \n", show_file_deleted(manifests))


if __name__ == "__main__":
    main()


import argparse

import compare_manifests

# set up argparse to take in file name as command line arg
parser = argparse.ArgumentParser()
parser.add_argument("file_name")
args = parser.parse_args()

target_file = args.file_name

manifests = compare_manifests.populate_manifest()

content_change_files = compare_manifests.show_hash_change(manifests)
name_change_files = compare_manifests.show_file_name_change(manifests)
added_files = compare_manifests.show_file_added(manifests)
deleted_files = compare_manifests.show_file_deleted(manifests)

summary_dict = {
    "content change": content_change_files,
    "name change": name_change_files,
    "added in": added_files ,
    "deleted": deleted_files,
}

target_dict = {}
for change, file_list in summary_dict.items():
    if target_file in file_list:
        if target_file in (manifests[(list(manifests.keys())[0])]) and target_file in (manifests[(list(manifests.keys())[1])]):
            target_dict[change] = [(list(manifests.keys())[0]), (list(manifests.keys())[1])]
        elif target_file in manifests[(list(manifests.keys())[0])]:
            target_dict[change] = (list(manifests.keys())[0])
        else:
            target_dict[change] = (list(manifests.keys())[1])

print(f"change history for {target_file}: \n")
for change, manifests in target_dict.items():
    print(f"{change}: {target_file} is in {manifests}")



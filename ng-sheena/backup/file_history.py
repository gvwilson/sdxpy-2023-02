import argparse

import compare_manifests

parser = argparse.ArgumentParser()

parser.add_argument("file_name")

args = parser.parse_args()

target_file = args.file_name

manifests = compare_manifests.populate_manifest()

content_change = compare_manifests.show_hash_change(manifests)
name_change = compare_manifests.show_file_name_change(manifests)
added = compare_manifests.show_file_added(manifests)
deleted = compare_manifests.show_file_deleted(manifests)

summary_dict = {
    "content change": content_change,
    "name change": name_change,
    "added in": added ,
    "deleted": deleted,
}

print(summary_dict)

target_dict = {}
for change, file_name_list in summary_dict.items():
    if target_file in file_name_list:
        target_dict[change] = list(manifests.keys())

print(f"change history for {target_file}: \n")

for change, manifests in target_dict.items():
    print(f"{change}: {target_file} is in {manifests}")



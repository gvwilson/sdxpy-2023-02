import csv
import glob

# A bit of a mess but... Seemingly works... Basically the way I want it to...

def file_history(file_name = "abc.txt", manifest_files = glob.glob(r"C:\Users\Fraser\Desktop\Homework\manifest*.csv")):
    manifests = []
    manifest_names = []

    for file in manifest_files:
        with open(file, 'r') as f:
            reader = csv.reader(f)
            next(reader) # Skip header row
            manifest = {}
            for row in reader:
                manifest[row[0]] = row[1]
            manifests.append(manifest)
            manifest_names.append(file.split('\\')[-1])

    # Find the first manifest where the file appears
    first_manifest_index = None
    for i, manifest in enumerate(manifests):
        if file_name in manifest:
            first_manifest_index = i
            print(f"{file_name}: {manifest[file_name]} (from manifest {manifest_names[first_manifest_index]})")
            break

    # Traverse the remaining manifests and track changes
    if first_manifest_index is not None:
        hash_value = manifests[first_manifest_index][file_name]
        deleted = False # Because it exists by default.
        for i in range(first_manifest_index+1, len(manifests)):
            manifest = manifests[i]
            if file_name in manifest:
                new_hash_value = manifest[file_name]
                if new_hash_value != hash_value:
                    print(f"{file_name}: {new_hash_value} (from manifest {manifest_names[i]})")
                    hash_value = new_hash_value
                deleted = False
            elif not deleted:
                print(f"{file_name} was deleted in manifest {manifest_names[i]}")
                hash_value = "<Deleted>"
                deleted = True
    else:
        print(f"{file_name} not found in any manifest")

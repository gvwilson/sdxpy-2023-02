import hashlib
import csv

def compare_manifests(manifest1 = r"C:\Users\Fraser\Desktop\Homework\a.csv", manifest2 = r"C:\Users\Fraser\Desktop\Homework\b.csv"):
    # Setup
    changes = {
        'changed_contents': [],
        'renamed': [],
        'deleted': [],
        'added': []
    }
    # Load the files
    manifests = []
    for m in [manifest1, manifest2]:
        with open(m, 'r') as f:
            reader = csv.reader(f)
            next(reader) # Skip the header row
            manifest = dict(row for row in reader)
            manifests.append(manifest)
    # Check: files with the same names but different hashes
    for i in set(manifests[0].keys()) & set(manifests[1].keys()):
        if manifests[0][i] != manifests[1][i]:
            changes['changed_contents'].append(i)
    # Check: files with the same hashes but different names --- Apparently I can't use "hash" as a variable name... 
    manifest_names1 = {}
    for i, h in manifests[0].items():
        manifest_names1[h] = i
    manifest_names2 = {}
    for i, h in manifests[1].items():
        manifest_names2[h] = i
    for h in set(manifests[0].values()) & set(manifests[1].values()):
        if manifest_names1[h] != manifest_names2[h]:
            changes['renamed'].append((manifest_names1[h], manifest_names2[h]))
    # Check: deleted files (from first to second) - exclude renames
    for i in set(manifests[0].keys()) - set(manifests[1].keys()) - set(*changes['renamed']):
        changes['deleted'].append(i)
    # Check: new files (in second but not first) - exclude renames
    for i in set(manifests[1].keys()) - set(manifests[0].keys()) - set(*changes['renamed']):
        changes['added'].append(i)    
    # All done
    return changes

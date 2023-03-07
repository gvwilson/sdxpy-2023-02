import sys
import csv

def read_manifests(path):
    """
        read csv file, covert it into a hash:name dict. 
    """
    hash2name = {}
    
    with open(path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:           
            hash2name[row["hash"]] = row["name"]
                
    return hash2name   

def compare(file1, file2):
    """
        compare two csv file, report how many records have been changed, 
        renamed, added or deleted from file1 to file2.
    """
    hash2name1 = read_manifests(file1)
    hash2name2 = read_manifests(file2)
    
    name2hash1 = {n: h for h, n in hash2name1.items()}
    name2hash2 = {n: h for h, n in hash2name2.items()}
    
    result = {"changed": [],
    "renamed": [],
    "added":  [],
    "deleted": []}
    
    for hash_code, name in hash2name1.items():
        if name in name2hash2 and name2hash1[name] != name2hash2[name]:
            result["changed"].append(name)
        if hash_code in hash2name2 and hash2name1[hash_code] != hash2name2[hash_code]:
            result["renamed"].append(name)
        if hash_code not in hash2name2 and name not in name2hash2:
            result["deleted"].append(name)
            
    new_names = name2hash2.keys() - name2hash1.keys()
    for name in new_names:
        if name2hash2[name] not in hash2name1:
            result["added"].append(name)
            
    return result

def main():
    assert len(sys.argv) == 3, "Usage: compare-manifests.py file1_name file2_name"

    result = compare(sys.argv[1], sys.argv[2])
    print(f"changed => {result['changed']}")
    print(f"renamed => {result['renamed']}")
    print(f"deleted => {result['deleted']}")
    print(f"added => {result['added']}")

if __name__ == "__main__":
    main()
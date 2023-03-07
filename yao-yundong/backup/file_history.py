import csv
import sys
import time
import os
from glob import glob

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
    
    result = []
    operation = None
    updated_time = time.ctime(os.path.getmtime(file2))


    for hash_code, name in hash2name2.items():
        if name in name2hash1 and name2hash1[name] != hash_code:
            operation = "changed"
        if hash_code in hash2name1 and hash2name1[hash_code] != name:
            operation = "renamed"
        if hash_code not in hash2name1 and name not in name2hash1:
            operation = "added"
        if operation:
            result.append([name, hash_code, operation, updated_time])
            
    deleted_names = name2hash1.keys() - name2hash2.keys()
    for name in deleted_names:
        if name2hash1[name] not in hash2name2:
            operation = "deleted"
            if operation:
                result.append([name, name2hash1[name], operation, updated_time])

            
    return result




def find_file_history(file_name):
    """find file in manifest by file name or hash, 
    return file name and hash if the file exist in the manifest, 
    else return None."""
    
    manifests = glob('manifest*.csv')
    manifests.sort(key=os.path.getmtime, reverse=True)
    logs = []
    hash_code = None
    # print(file_name)
    for  manifest1,  manifest2 in zip(manifests[1:], manifests[:-1]):
        print(manifest1,  manifest2)
        report = compare(manifest1,  manifest2)
        # print(report)
        for rec in report:
            if file_name == rec[0] or hash_code == rec[1]:
                file_name = rec[0]
                hash_code = rec[1]
                logs.append(rec)
    # print(logs)
    assert logs, "Could not find this file"

    return logs


def main():
    assert len(sys.argv) == 2, "Usage: file_history.py file_name"

    result = find_file_history(sys.argv[1])
    for r in result[::-1]:
        print(r)

if __name__ == "__main__":
    main()
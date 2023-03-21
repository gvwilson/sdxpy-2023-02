import hashlib
import os
import glob

def find_dupes(file_list = glob.glob(r"C:\Users\Fraser\Desktop\Homework\manifest*.csv")):
    file_hashes = {}
    for file in file_list:
        with open(file, 'rb') as f: # Remember to open for binary reading here.
            file_hash = hashlib.md5(f.read()).hexdigest() # Calculate hash of the file
            if file_hash in file_hashes: # If the hash already exists, add filename to the list of duplicates
                file_hashes[file_hash].append(file)
            else:  # add new hash to the dictionary
                file_hashes[file_hash] = [file]

    # This way of iterating is new to me, but obviously quite powerful...
    duplicates = {hash_value: filenames for hash_value, filenames in file_hashes.items() if len(filenames) > 1}

    if not duplicates:  # if no duplicates found
        print("No duplicates found.")
        return
    print("Duplicates found:\n")
    for hash_value, filenames in duplicates.items():
        print("Hash:", hash_value)
        for filename in filenames:
            print(filename)

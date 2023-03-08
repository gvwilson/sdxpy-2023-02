#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 13:46:39 2023

@author: beccalove
"""

import hashlib
from pathlib import Path
import numpy as np
import sys

#BUFFER_SIZE = 4 * 1024

def hash_stream(infile, buffer_size = 4 * 1024):
    
    sha256 = hashlib.sha256()
    
    while True:
        block = infile.read(buffer_size)
        if not block:
            break
        sha256.update(block)
        
    return sha256.hexdigest()

def calculate_hashes(list_of_paths):
    
    hash_dict = {}
    
    for path in list_of_paths:
        
        with open (Path(path), "rb") as infile:
            hash_code = hash_stream(infile)
            hash_dict[path] = hash_code
            
    return hash_dict

def find_dups(hash_dict):
    
    paths = np.array(list(hash_dict.keys()))
    hashes = np.array(list(hash_dict.values()))
        
    unique_hashes, hash_counts = np.unique(hashes, return_counts=True)
    
    repeated_hashes = unique_hashes[hash_counts > 1]
    
    return(paths[np.isin(hashes, repeated_hashes)])
    
def main(paths):
    
    hash_dict = calculate_hashes(paths)
    dups = find_dups(hash_dict)
    print(dups)
    
    #return dups
    
if __name__ == "__main__":
    
    paths = sys.argv[1:]
    main(paths)

    

"""
import argparse
from collections import defaultdict
import csv
import numpy as np
import os

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file1", help="path to earlier checkpoint")
    parser.add_argument("file2", help="path to later checkpoint")
    args = parser.parse_args()
    return args

def read_files(file1, file2):
    files_dict = defaultdict(dict)
    
    for path in [file1, file2]:
        name = os.path.basename(path)
        
        with open(path) as infile:
            
            inreader = csv.reader(infile, delimiter='\t')
            for row in inreader:
                files_dict[name][row[0]] = row[1]
                
    return files_dict

def compare_hashes(files_dict):
    
    assert len(files_dict) == 2, "Comparing more than 2 files is not supported"
    
    contents_changed = []
    renamed = []
    deleted = []
    added = []
    
    manifest1 = list(files_dict.keys())[0]
    manifest2 = list(files_dict.keys())[1]
    
    files1 = np.array(list(files_dict[manifest1].keys()))
    files2 = np.array(list(files_dict[manifest2].keys()))
    
    hashes1 = np.array(list(files_dict[manifest1].values()))
    hashes2 = np.array(list(files_dict[manifest2].values()))
    
    for file in files1:
        if file in files2:
            if files_dict[manifest1][file] == files_dict[manifest2][file]:
                continue
            else:
                contents_changed.append(file)
                
        else:
            
            if files_dict[manifest1][file] in hashes2:
                renamed.append(file)
            else:
                deleted.append(file)
                
    for file in files2:
        if file not in files1:
            if files_dict[manifest2][file] not in hashes1:
                added.append(file)
                
    print(f"contents changed: {[file for file in contents_changed]}\n")
    print(f"renamed: {[file for file in renamed]}\n")
    print(f"deleted: {[file for file in deleted]}\n")
    print(f"added: {[file for file in added]}\n")
            
    
def main(args):
    files_dict = read_files(args.file1, args.file2)
    compare_hashes(files_dict)
    
if __name__ == "__main__":
    
    args = parse_args()
    main(args)
    
"""

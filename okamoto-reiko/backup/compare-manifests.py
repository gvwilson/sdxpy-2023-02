import sys
import pandas as pd

def compare_manifests(file_a, file_b):
    
    # read in manifest A
    csv_a = pd.read_csv(file_a)    
    manifest_a = {'name': csv_a['name'].values.tolist(),
                  'hash': csv_a['hash'].values.tolist()} # probably a more elegant way to read in these files...
    
    # read in manifest B
    csv_b = pd.read_csv(file_b)    
    manifest_b = {'name': csv_b['name'].values.tolist(),
                  'hash': csv_b['hash'].values.tolist()}
    
    # define dictionary to store results
    results = {'changed': [],
               'renamed': [],
               'deleted': [],
               'added'  : []}
    
    for i in range(len(manifest_a['name'])):
        # file name exists in both places
        if manifest_a['name'][i] in manifest_b['name']: 
            index_b = manifest_b['name'].index(manifest_a['name'][i])
            if manifest_a['hash'][i] != manifest_b['hash'][index_b]: # but have different hashes (content has changed)
                results['changed'].append(manifest_a['name'][i])
    
        # hash exists in both places
        if manifest_a['hash'][i] in manifest_b['hash']: 
            index_b = manifest_b['hash'].index(manifest_a['hash'][i])
            if manifest_a['name'][i] != manifest_b['name'][index_b]: # but have different names 
                results['renamed'].append(manifest_a['name'][i])
            
        # name/hash exists in manifest A, but not in B 
        if (not manifest_a['name'][i] in manifest_b['name']) & (not manifest_a['hash'][i] in manifest_b['hash']):
            results['deleted'].append(manifest_a['name'][i]) 
            
    for i in range(len(manifest_b['name'])):
        # name/hash exists in manifest B, but not in A
        if (not manifest_b['name'][i] in manifest_a['name']) & (not manifest_b['hash'][i] in manifest_a['hash']):
            results['added'].append(manifest_b['name'][i])
            
    return(results)

def main():
    assert len(sys.argv) == 3, "Usage: func.py manifest_a.csv manifest_b.csv"    
    results = compare_manifests(sys.argv[1], sys.argv[2])
    print(f"=> {results}")
    
if __name__ == "__main__":
    main()

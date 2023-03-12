import sys
import hashlib

# code attribution: Greg Wilson, lecture 3
def hash_stream(reader):
    sha256 = hashlib.sha256()
    while True:
        block = reader.read(4 * 1024)
        if not block:
            break
        sha256.update(block)
    return sha256.hexdigest()

def finddup(filenames):
    
    results = {}
    
    # calculate hash
    for file in filenames:
        reader = open(file, "rb")
        hash_out = hash_stream(reader)
        
        if not hash_out in results.keys():
            results[hash_out] = [file]
        else:
            results[hash_out].append(file)
            
    dups = {k:v for (k,v) in results.items() if len(v) > 1} # only return duplicates
            
    return(dups)

def main():   
    results = finddup(sys.argv[1:])
    print(f"=> {results}")
    
if __name__ == "__main__":
    main()
    
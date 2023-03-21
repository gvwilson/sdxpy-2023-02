import sys
from compare_manifests import compare_manifests, read_manifests
from pprint import pprint

filename = sys.argv[1]
manifests = read_manifests("backup_dir")

for i in range(0, len(manifests) - 1):
    res = compare_manifests(manifests[i : i + 2])
    pprint(res)
    print("*****")

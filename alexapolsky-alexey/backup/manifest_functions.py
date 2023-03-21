import csv
import glob
import os.path
from pathlib import Path
from functools import cache


def read_manifest(manifest_file):
    manifest_file = Path(manifest_file)
    rows = []
    with open(manifest_file, "r") as raw:
        reader = csv.reader(raw)
        for row in reader:
            rows.append(row)
    return rows


def read_manifests(backup_dir):
    result = []

    for filename in sorted(
        glob.glob("backup_dir/manifest*.csv", recursive=False),
        key=os.path.abspath,
        reverse=False,
    ):
        full_name = filename
        with open(full_name, "rb") as reader:
            manifest = read_manifest(full_name)
            result.append(manifest)
    return result

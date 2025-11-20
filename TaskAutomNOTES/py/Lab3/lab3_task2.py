#!/usr/bin/env python3
import sys

def main():
    # python lab3.py md5_og.txt md5_new.txt

    og_file = sys.argv[1]
    new_file = sys.argv[2]

    og_names = []
    orig_hashes = []

    f = open(og_file, "r")
    for line in f:
        line = line.strip()
        if len(line) == 0:
            continue

        parts = line.split()
        if len(parts) != 2:
            continue

        filename = parts[0]
        md5_value = parts[1]

        og_names.append(filename)
        orig_hashes.append(md5_value)

    f.close()

    new_names = []
    new_hashes = []

    f = open(new_file, "r")
    for line in f:
        line = line.strip()
        if len(line) == 0:
            continue

        parts = line.split()
        if len(parts) != 2:
            continue

        filename = parts[0]
        md5_value = parts[1]

        new_names.append(filename)
        new_hashes.append(md5_value)

    f.close()

    i = 0
    while i < len(og_names):
        orig_name = og_names[i]
        orig_md5 = orig_hashes[i]
        new_md5 = new_hashes[i]

        if orig_md5 != new_md5:
            print(orig_name + ": MD5 original = " + orig_md5 + ", MD5 new = " + new_md5)
        i += 1



main()

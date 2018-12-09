#!/usr/bin/env python3

import re
import sys
import tarfile

TAR = sys.argv[1]
NUM = sys.argv[2]

def main():
    for f in tarfile.open(TAR, mode='r:gz'):
        filename = f.name

if __name__ == "__main__":
    main()

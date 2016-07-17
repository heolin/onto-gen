#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

def main():
    count = 0
    for f in os.listdir(sys.argv[1]):
        for line in open(sys.argv[1]+"/"+f).read().split('\n'):
            output_file = open(sys.argv[2]+"/"+str(count)+".txt", 'w')
            output_file.write(line+"\n")
            output_file.close()
            count += 1

if __name__ == "__main__":
    main()

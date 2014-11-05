#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT


def lemmatize_word(word):
    args = ["/home/heolin123/Libraries/morfologik-distribution-1.9.0/morfologik-tools-1.9.0-standalone.jar", "plstem"]
    process = Popen(['java', '-jar']+list(args), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    stdout = process.communicate('testuje')[0]
    process.stdin.close()

    return stdout.split('\n')[4].split('\t')[1]


def main():
    print lemmatize_word("testuje")


if __name__ == "__main__":
    main()

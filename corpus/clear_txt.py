#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys
import re
import argparse

SENTENCE_SEPARATORS = ".!?\'\"\(\)\[\]\}\{"
TOKEN_SEPARATORS = " \−\-;,.!?\'\"\(\)\[\]\}\{"

stopwords = []
blacklist = []

DOT = " "

MINIMAL_LINE_LENGTH = 20

def handle_abbreviation(line):
    line = line.replace("prof.", "prof"+DOT)
    line = line.replace("mgr.", "mgr"+DOT)
    line = line.replace("dr.", "dr"+DOT)
    line = line.replace("r.", "r"+DOT)
    line = line.replace("inż.", "inż"+DOT)
    line = line.replace("hab.", "hab"+DOT)
    line = line.replace("nzw.", "nzw"+DOT)
    line = line.replace("arch.", "arch"+DOT)
    line = line.replace("tel.", "tel"+DOT)
    line = line.replace("godz.", "godz"+DOT)
    line = line.replace("m.in.", "m"+DOT+"in"+DOT)
    line = line.replace("Sz.P.", "Sz"+DOT+"P"+DOT)
    line = line.replace("m.st.", "m"+DOT+"st"+DOT)
    line = line.replace("p.n.e.", "p"+DOT+"n"+DOT+"e")
    line = line.replace("np.", "np"+DOT)
    line = line.replace("ul.", "ul"+DOT)
    line = line.replace("ur.", "ur"+DOT)
    line = line.replace("mm.", "mm"+DOT)
    line = line.replace("dypl.", "dypl"+DOT)
    line = line.replace("zm.", "zm"+DOT)
    return line

def split(line):
    return re.findall("[^"+SENTENCE_SEPARATORS+"]+", line)

def tokenize(line):
    result = re.findall("[^"+TOKEN_SEPARATORS+"]+", line)
    return result


def clear(token):
    token = re.sub("^ ", "", token)
    if re.match("^[A-Za-z\x88-\xFF]*$", token):
        token = token.lower();
        if token in stopwords:
            return ""
        if len(token) < 3:
            return ""
        return token
    return ""

def clear_sentence(sentence):
    if len(sentence) < MINIMAL_LINE_LENGTH:
        return ""
    result = [clear(token) for token in tokenize(sentence)]
    for token in result:
        if token in blacklist:
            return ""
    result = filter(None, result) 
    return " ".join(result)


def main():
    global blacklist
    global stopwords

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--blacklist", help="Path to file with blacklist.")
    parser.add_argument("-s", "--stopwords", help="Path to file with list of stopwords.")
    args = parser.parse_args(sys.argv[1:])

    if args.blacklist:
        blacklist = open(args.blacklist).read().split('\n')[:-1]

    if args.stopwords:
        stopwords = open(args.stopwords).read().split('\n')[:-1]

    rest = ""
    for line in sys.stdin:
        line = rest + line
        line = handle_abbreviation(line.replace('\n', ' '))

        splited = split(line)

        if splited > 1:
            for result in [clear_sentence(seg) for seg in splited[:-1]]:
                if result != "":
                    if len(result) > MINIMAL_LINE_LENGTH:
                        print result

        rest = splited[-1]

if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import argparse

from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT

process = None
MISSED = 'missed'
NEXT_LINE = "NEXTLINE"

def normalize(input_text):
    result = input_text
    if len(result) == 0:
        return None
    result = result[0].lower() + result[1:]
    result = re.sub('[.,?!]', '', result)
    return result


def lemmatize(word, close=False):
    args = ["/home/heolin123/Libraries/morfologik-distribution-1.9.0/morfologik-tools-1.9.0-standalone.jar", "plstem"]
    process = Popen(['java', '-jar']+list(args), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    stdout = process.communicate(word)[0]
    process.stdin.close()
    result = stdout.split('\n')
    process.stdin.close()
    return result[4:-2]


def parse_data(lemma_data):
    lemma_data[2] = [r.split(':') for r in lemma_data[2].split('+')]
    pos = list(set([r[0] for r in lemma_data[2]]))
    return [lemma_data[0], lemma_data[1], pos]


def filter_data(lemma_data):
    if len(lemma_data) == 0:
        return []
    result = [lemma_data[0]]
    for lemma in lemma_data:
        if result[-1][0] != lemma[0]:
            result.append(lemma)
        else:
            result[-1][2].extend(lemma[2])
    for lemma in result:
        if lemma[1] == "-":
            lemma[1] = lemma[0]
            lemma[2] = ['subst', MISSED]
        lemma[2] = tuple(set([r for r in lemma[2]]))
    return result


def split(data):
    sentences = []
    current_sentence = []
    for token in data:
        token_data = token.split("\t")
        if token_data[0] == NEXT_LINE:
            if len(current_sentence) > 0:
                sentences.append(current_sentence)
            current_sentence = []
        else:
            current_sentence.append(token_data)
    if len(current_sentence) > 0:
        sentences.append(current_sentence)
    return sentences


def process_text(text):
    norm_text = normalize(text)
    lemma_data = lemmatize(norm_text)
    sentences = split(lemma_data)
    return sentences

def process_sentence(lemma_data):
    lemma_data = [parse_data(lemma) for lemma in lemma_data]
    sentence_data = filter_data(lemma_data)
    return sentence_data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Path to file with input data.", required=True)

    args = parser.parse_args(sys.argv[1:])

    input_text = open(args.input).read().split('\n')[:-1]

    join_str = "\n{}\n".format(NEXT_LINE)
    sentence_data = process_text(join_str.join(input_text))
    for sentence in sentence_data:
        sentence_data = process_sentence(sentence)
        print " ".join([data[1] for data in sentence_data[1:]])


if __name__ == "__main__":
    main()

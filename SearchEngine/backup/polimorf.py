#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------

import sys
import os

PATH = "poli.dic"
PATH_TEMP = "poli_temp.dic"
MORPF_PATH = "/home/heolin123/Documents/NLP/PoliMorf/PoliMorf_sorted.tsv"

N = 3

class Lemmatizer(object):

    morpf_dictionary = {}
    dictionary = None

    def __init__(self):
        if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
            self.load()
        else:
            self.generate()

    def generate(self):
        input_file = open(MORPF_PATH)

        morpf_list = []

        last = ""
        line = 1
        while line:
            line = input_file.readline().lower().decode('utf-8')

            if '\t' not in line:
                continue

            line = line[:line.index('\t')]
            length = min(N, len(line))

            if line[:length] != last:
                last = line[:length]
                morpf_list.append((last, input_file.tell()))

        input_file.close()


        output_file = open(PATH_TEMP, "w")

        for line in morpf_list:
            output_line = u"{0}\t{1}\n".format(line[0], line[1])
            output_file.write(output_line.encode('utf-8'))

        output_file.close()


    def load(self):

        for line in open(PATH).read().split('\n'):
            splited = line.split('\t')
            if len(splited) > 1:
                self.morpf_dictionary[splited[0]] = int(splited[1])
        self.dictionary = open(MORPF_PATH)


    def lemmatize_word(self, word):
        word = word.lower()

        length = min(N, len(word))
        line_length = length

        index = word[:length]
        line_index = index

        if index not in self.morpf_dictionary:
            return word

        self.dictionary.seek(self.morpf_dictionary[index])

        fallback_count = 1000

        while line_index == index:
            line = self.dictionary.readline()
            line_index = line[:min(length, len(line))]
            line_splited = line.split('\t')

            if line_splited[0] == word:
                return line_splited[1]

            fallback_count -= 1
            if fallback_count < 0:
                return word
        return word




def main():
    lemmatizer = Lemmatizer()
    for line in sys.stdin:
        print lemmatizer.lemmatize_word(line.replace("\n", ""))

if __name__ == "__main__":
    main()

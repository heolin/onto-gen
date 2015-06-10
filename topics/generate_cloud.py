#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse

from pytagcloud import create_tag_image, make_tags, LAYOUT_HORIZONTAL, LAYOUT_VERTICAL, LAYOUT_MOST_HORIZONTAL, LAYOUT_MOST_VERTICAL, LAYOUT_MIX
from pytagcloud.colors import COLOR_SCHEMES
from pytagcloud.lang.counter import get_tag_counts

from gensim import corpora, models

def process_token(token, wage):
    return (token, wage)

def generate_image(wordscount, output_path):
    tags = make_tags(wordscount, minsize=10, maxsize=60)
    create_tag_image(tags, output_path, size = (800,800), layout=LAYOUT_MIX, background=(0, 0, 0, 255), fontname='PT Sans Regular')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lsi', help="Input path to model text file.")
    parser.add_argument('-o', "--out", required=True, help="Ouput path form images.")
    args = parser.parse_args()

    if args.lsi:
        lsimodel = models.LsiModel.load(args.lsi)
        name = "/lsi_{}.txt"
        index = 0
        for topic in lsimodel.show_topics(num_topics=5, num_words=40, formatted=False):
            wordscount = []
            for word in topic:
                wordscount.append(process_token(word[1], abs(word[0]*10)))
            output_file = open(args.out + name.format(index), 'w')
            words_list = []
            for word in wordscount:
                for _ in xrange((int)(word[1]*100)):
                    words_list.append(word[0].encode('utf-8'))
            output_file.write(" ".join(words_list))
            output_file.close()

            #generate_image(wordscount, )
            index += 1


if __name__ == "__main__":
    main()

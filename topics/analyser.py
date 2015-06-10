#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from gensim import corpora, models, similarities

import os
import argparse

STOP_WORDS = set([u'a', u'acz', u'aczkolwiek', u'aj', u'albo', u'ale', u'ależ', u'ani', u'aż', u'bardziej', u'bardzo', u'bo', u'bowiem', u'by', u'byli', u'bynajmniej', u'być', u'był', u'była', u'było', u'były', u'będzie', u'będą', u'cali', u'cała', u'cały', u'ci', u'cię', u'ciebie', u'co', u'cokolwiek', u'coś', u'czasami', u'czasem', u'czemu', u'czy', u'czyli', u'daleko', u'dla', u'dlaczego', u'dlatego', u'do', u'dobrze', u'dokąd', u'dość', u'dużo', u'dwa', u'dwaj', u'dwie', u'dwoje', u'dziś', u'dzisiaj', u'gdy', u'gdyby', u'gdyż', u'gdzie', u'gdziekolwiek', u'gdzieś', u'i', u'ich', u'ile', u'im', u'inna', u'inne', u'inny', u'innych', u'iż', u'ja', u'ją', u'jak', u'jakaś', u'jakby', u'jaki', u'jakichś', u'jakie', u'jakiś', u'jakiż', u'jakkolwiek', u'jako', u'jakoś', u'je', u'jeden', u'jedna', u'jedno', u'jednak', u'jednakże', u'jego', u'jej', u'jemu', u'jest', u'jestem', u'jeszcze', u'jeśli', u'jeżeli', u'już', u'ją', u'każdy', u'kiedy', u'kilka', u'kimś', u'kto', u'ktokolwiek', u'ktoś', u'która', u'które', u'którego', u'której', u'który', u'których', u'którym', u'którzy', u'ku', u'lat', u'lecz', u'lub', u'ma', u'mają', u'mało', u'mam', u'mi', u'mimo', u'między', u'mną', u'mnie', u'mogą', u'moi', u'moim', u'moja', u'moje', u'może', u'możliwe', u'można', u'mój', u'mu', u'musi', u'my', u'na', u'nad', u'nam', u'nami', u'nas', u'nasi', u'nasz', u'nasza', u'nasze', u'naszego', u'naszych', u'natomiast', u'natychmiast', u'nawet', u'nią', u'nic', u'nich', u'nie', u'niech', u'niego', u'niej', u'niemu', u'nigdy', u'nim', u'nimi', u'niż', u'no', u'o', u'obok', u'od', u'około', u'on', u'ona', u'one', u'oni', u'ono', u'oraz', u'oto', u'owszem', u'pan', u'pana', u'pani', u'po', u'pod', u'podczas', u'pomimo', u'ponad', u'ponieważ', u'powinien', u'powinna', u'powinni', u'powinno', u'poza', u'prawie', u'przecież', u'przed', u'przede', u'przedtem', u'przez', u'przy', u'roku', u'również', u'sam', u'sama', u'są', u'się', u'skąd', u'sobie', u'sobą', u'sposób', u'swoje', u'ta', u'tak', u'taka', u'taki', u'takie', u'także', u'tam', u'te', u'tego', u'tej', u'temu', u'ten', u'teraz', u'też', u'to', u'tobą', u'tobie', u'toteż', u'trzeba', u'tu', u'tutaj', u'twoi', u'twoim', u'twoja', u'twoje', u'twym', u'twój', u'ty', u'tych', u'tylko', u'tym', u'u', u'w', u'wam', u'wami', u'was', u'wasz', u'wasza', u'wasze', u'we', u'według', u'wiele', u'wielu', u'więc', u'więcej', u'wszyscy', u'wszystkich', u'wszystkie', u'wszystkim', u'wszystko', u'wtedy', u'wy', u'właśnie', u'z', u'za', u'zapewne', u'zawsze', u'ze', u'zł', u'znowu', u'znów', u'został', u'żaden', u'żadna', u'żadne', u'żadnych', u'że', u'żeby'])


class CorpusIterator(object):
    def __init__(self, corpus_path, dictionary):
        self.corpus_path = corpus_path
        self.dictionary = dictionary

    def __iter__(self):
        for line in open(self.corpus_path):
            splited = [word for word in line.lower().split() if word not in STOP_WORDS]
            yield self.dictionary.doc2bow(splited)

def analyse(input_path):
    file_name, _ = os.path.splitext(input_path)

    dictionary = corpora.Dictionary(line.lower().split() for line in open(input_path))

    stop_ids = [dictionary.token2id[stopword] for stopword in STOP_WORDS\
            if stopword in dictionary.token2id]

    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems()\
            if docfreq == 1]

    dictionary.filter_tokens(stop_ids + once_ids)
    dictionary.compactify()
    dictionary.save(file_name + '.dict')

    corpus = CorpusIterator(input_path, dictionary)
    corpora.MmCorpus.serialize(file_name + '.mm', corpus)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help="Input path to corpus text file.")
    args = parser.parse_args()
    analyse(args.input)


if __name__ == "__main__":
    main()



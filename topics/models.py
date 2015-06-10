#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from gensim import corpora, models

import os
import argparse


def get_tfidf_model(corpus):
    return models.TfidfModel(corpus)

def get_lsi_model(corpus_tfidf, dictionary, topics=10):
    return models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=topics)

def get_lda_model(corpus_tfidf, dictionary, topics=10):
    return models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=topics)

def get_rp_model(corpus_tfidf, dictionary, topics=10):
    return models.RpModel(corpus_tfidf, id2word=dictionary, num_topics=topics)


def create_models(corpus_path):
    file_name, _ = os.path.splitext(corpus_path)

    dictionary = corpora.Dictionary.load(file_name + '.dict')
    corpus = corpora.MmCorpus(file_name + '.mm')

    tfidf_model = get_tfidf_model(corpus)

    corpus_tfidf = tfidf_model[corpus]

    rp_model = get_rp_model(corpus_tfidf, dictionary)
    lsi_model = get_lsi_model(corpus_tfidf, dictionary)
    lda_model = get_lda_model(corpus_tfidf, dictionary)

    tfidf_model.save(file_name + ".tfidfmodel")
    lsi_model.save(file_name + ".lsimodel")
    lda_model.save(file_name + ".ldamodel")
    rp_model.save(file_name + ".rpmodel")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help="Input path to corpus text file.")
    args = parser.parse_args()

    create_models(args.input)


if __name__ == "__main__":
    main()



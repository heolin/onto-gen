#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from gensim import corpora, models, similarities, matutils

import os
import argparse
from collections import OrderedDict


class TopicsManager(object):
    def __init__(self, corpus_dir, default=True):
        file_name, _ = os.path.splitext(corpus_dir)

        self.corpus_path = file_name
        self.dictionary = corpora.Dictionary.load(file_name + '.dict')
        self.corpus = corpora.MmCorpus(file_name + '.mm')
        self.lsi_term_corpus = None
        self.lda_term_corpus = None
        if default:
            self.load_default()

    def load_default(self):
        self.load_tfidf_model()
        self.load_lsi_model()
        self.load_lsi_similarity_matrix()

    def load_tfidf_model(self):
        self.tfidf_model = models.TfidfModel.load(self.corpus_path + ".tfidfmodel")


    def load_lsi_model(self):
        self.lsi_model = models.LsiModel.load(self.corpus_path + ".lsimodel")

    def load_lda_model(self):
        self.lda_model = models.LdaModel.load(self.corpus_path + ".ldamodel")

    def load_rp_model(self):
        self.rpmodel = models.RpModel.load(self.corpus_path + ".rpmodel")

    def get_lsi_topics(self, topics=5, words=15):
        return self.lsi_model.show_topics(num_topics=topics, num_words=words, formatted=False)

    def save_lsi_similarity_matrix(self):
        self.lsi_term_corpus = matutils.Dense2Corpus(self.lsi_model.projection.u.T)
        self.similarity_matrix = similarities.MatrixSimilarity(self.lsi_term_corpus)
        self.similarity_matrix.save(self.corpus_path + ".lsisimmatrix")

    def save_lda_similarity_matrix(self):
        self.lda_term_corpus = matutils.Dense2Corpus(self.lda_model.state.get_lambda())
        self.similarity_matrix = similarities.MatrixSimilarity(self.lda_term_corpus)
        self.similarity_matrix.save(self.corpus_path + ".ldasimmatrix")

    def load_lsi_similarity_matrix(self):
        self.similarity_matrix = similarities.MatrixSimilarity.load(self.corpus_path + ".lsisimmatrix")
        self.lsi_term_corpus = list(matutils.Dense2Corpus(self.lsi_model.projection.u.T))

    def load_lda_similarity_matrix(self):
        self.similarity_matrix = similarities.MatrixSimilarity.load(self.corpus_path + ".ldasimmatrix")
        self.lda_term_corpus = list(matutils.Dense2Corpus(self.lda_model.state.get_lambda()))

    def get_similarity(self, word1, word2):
        if word1 not in self.dictionary.token2id:
            return 0

        if word2 not in self.dictionary.token2id:
            return 0

        word1_id = self.dictionary.token2id[word1]
        word2_id = self.dictionary.token2id[word2]

        query = self.lsi_term_corpus[word1_id]
        sims = self.similarity_matrix[query]

        similarity = sims[word2_id]
        return (similarity + 1) / float(2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help="Input path to corpus text file.")
    #parser.add_argument('-w1', '--word1', required=True, help="First input word.")
    #parser.add_argument('-w2', '--word2', required=True, help="Second input word.")
    parser.add_argument('-lda', '--lda', action="store_true", help="Second input word.")
    parser.add_argument('-s', '--save', action="store_true", help="Second input word.")
    args = parser.parse_args()

    topics_manager = TopicsManager(args.input)
    topics_manager.load_tfidf_model()
    if args.lda:
        topics_manager.load_lda_model()
        if args.save:
            topics_manager.save_lda_similarity_matrix()
        topics_manager.load_lda_similarity_matrix()
    else:
        topics_manager.load_lsi_model()
        if args.save:
            topics_manager.save_lsi_similarity_matrix()
        topics_manager.load_lsi_similarity_matrix()

    #print topics_manager.get_similarity(args.word1, args.word2)
    for topic in topics_manager.get_lsi_topics():
        print topic

if __name__ == "__main__":
    main()




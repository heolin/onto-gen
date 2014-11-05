#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
import unicodedata
import sys
import os
import json

from engine_utils import *

class SearchEngine(object):
    documents = {}
    inverted = []
    lang = POLISH

    def __init__(self, lang=""):
        self.documents = {}
        self.inverted = {}
        if lang != "":
            self.lang = lang

    def save(self, file_path):
        json.dump(self.inverted, open(file_path, 'w'))

    def load(self, file_path):
        self.inverted = json.load(open(file_path))


    @classmethod
    def from_json(cls, file_path):
        result = cls()
        result.load(file_path)
        result.update()
        return result

    @classmethod
    def from_directory(cls, directory_path, save_path=""):
        result = cls()
        for file_path in os.listdir(directory_path):
            if file_path.endswith(".txt"):
                path = directory_path + "/" + file_path
                file_name = file_path[:-4]
                file_text = open(path).read()
                result.add_document(file_name, file_text)
        result.update()
        if save_path != "":
            result.save(save_path)
        return result

    def add_document(self, document_name, document):
        self.documents[document_name] = document


    def update(self):
        for doc_id, text in self.documents.iteritems():
            doc_index = self.inverted_index(text)
            self.inverted_index_add(doc_id, doc_index)

    def inverted_index(self, text):
        """
        Create an Inverted-index of the specified text document.
            {word:[locations]}
        """
        inverted = {}
        for index, word in word_index(text, self.lang):
            locations = inverted.setdefault(word, [])
            locations.append(index)
        return inverted

    def inverted_index_add(self, doc_id, doc_index):
        """
        Add Invertd-Index doc_index of the document doc_id to the
        Multi-Document Inverted-Index (inverted),
        using doc_id as document identifier.
            {word:{doc_id:[locations]}}
        """
        for word, locations in doc_index.iteritems():
            indices = self.inverted.setdefault(word, {})
            indices[doc_id] = locations


    def print_inverted_index(self):
        for word, doc_locations in self.inverted.iteritems():
            if len(doc_locations) > 5:
                print word#, doc_locations


    def search(self, query):
        """
        Returns a set of documents id that contains all the words in your query.
        """
        words = [word for _, word in word_index(query, self.lang) if word in self.inverted]
        results = [set(self.inverted[word].keys()) for word in words]
        return reduce(lambda x, y: x & y, results) if results else []


    def search_text(self, query, around=20):
        query = query.encode('utf-8')
        result_docs = self.search(query)
        print u"Search for '{0}': {1}".format(query.decode('utf-8'), result_docs)

        for doc in result_docs:
            for _, word in word_index(query):
                for index in self.inverted[word][doc]:
                    print self.extract_text(doc, index, around, around + len(query)) + "\n"


    def extract_text(self, doc, index, around, around2):
        return self.documents[doc][index-around:index+around2].replace('\n', ' ').replace('\r', '')


    def get_cosine_simmilarity(self, term1, term2):
        term1_vector = {}
        term2_vector = {}
        if term1 in self.inverted:
            for term in  self.inverted[term1].keys():
                term1_vector[term] = len(self.inverted[term1])
        if term2 in self.inverted:
            for term in  self.inverted[term2].keys():
                term2_vector[term] = len(self.inverted[term2])
        return get_cosine(term1_vector, term2_vector)


if __name__ == '__main__':
    if sys.argv[1] == "json":
        engine = SearchEngine.from_json(sys.argv[2])
        engine.print_inverted_index()
    if sys.argv[1] == "dir":
        file_path = ""
        if len(sys.argv) > 2:
            file_path = sys.argv[3]
        engine = SearchEngine.from_directory(sys.argv[2], file_path)
    # Build Inverted-Index for documents


#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, ID, STORED, KEYWORD, TEXT, NUMERIC, BOOLEAN, DATETIME, NGRAM
from whoosh.qparser import QueryParser
import vector
#from vector import get_standard_vectors_union, get_standard_vector, get_full_vector

import os
import argparse
import sys

SCHEMA_PATH = "schema.tsv"

def message(*arguments):
    sys.stderr.write("[SEARCH_MANAGER]: " +' '.join(map(str, arguments)) + '\n')

class SearchManager(object):
    """Wrapper for Whoosh full-text quering system."""

    def __init__(self, indexdir, input_schema_path, verbose=False):
        self.indexdir = indexdir
        self.schema_path = input_schema_path
        self.index = None
        self.schema = None
        self.fields = []
        self.default_field = None
        self.index_writer = None
        self.verbose = verbose
        self.searcher = None

        self.set_schema()
        self.create_index()
        self.open_index()

        self.searcher = self.index.searcher()


    def message(self, arguments):
        if self.verbose:
            message(arguments)


    def set_schema(self):
        """Reads schema file from given path and parses it to Schema object."""

        if self.schema_path == None:
            if os.path.exists(self.indexdir):
                self.schema_path = self.indexdir + "/" + SCHEMA_PATH
            else:
                raise Exception('Error', 'No schema file found. Please create index and provide schema file.')
        schema_data = []
        schema_lines = open(self.schema_path).read().split('\n')[:-1]
        for line in schema_lines:
            splited = line.split('\t')
            field = splited[0]
            self.fields.append(field)
            f_type = splited[1]
            stored = ""
            if len(splited) >= 3:
                stored = "(stored=" + splited[2] + ")"
            if len(splited) == 4:
                self.default_field = splited[0]
            schema_data.append("{}={}{}".format(field, f_type, stored))
        if self.default_field == None:
            self.default_field = self.fields[0]
        self.schema = eval("Schema(" + ", ".join(schema_data) + ")")
        self.message("Loaded schema: " + str(self.schema)+ ".")
        self.message("Default field is set to: " + self.default_field + ".")


    def create_index(self):
        """If index directory does not exists, this method creates directory, creates index and saves schema file."""

        if not os.path.exists(self.indexdir):
            os.mkdir(self.indexdir)
            self.message("Created index at \"" + self.indexdir + "\".")
            create_in(self.indexdir, self.schema)
            with open(self.indexdir + "/" + SCHEMA_PATH, 'w') as output:
                output.write(open(self.schema_path).read())
                self.message("Saved schema to " + self.indexdir + "/" + SCHEMA_PATH + ".")


    def open_index(self):
        """Opens index from saved directory."""

        self.index = open_dir(self.indexdir)
        self.message("Loaded index from \"" + self.indexdir + "\".")


    def add_document(self, line):
        splited = line.decode('utf-8').split('\t')
        data = []
        for index in xrange(len(splited)):
            data.append(u"{}=u\"{}\"".format(self.fields[index], splited[index]))
        eval(u"self.index_writer.add_document({})".format(", ".join(data)))
        self.message(u"Added line to index: \"{}\".".format(splited[index]))


    def add_file(self, file_path):
        self.message("Adding file: {} to index.".format(file_path))
        self.index_writer = self.index.writer()
        for line in open(file_path).read().split('\n')[:-1]:
            self.add_document(line)
        self.index_writer.commit()

    def add_directory(self, directory_path):
        self.message("Adding directory: {} to index.".format(directory_path))
        self.index_writer = self.index.writer()
        for file_path in os.listdir(directory_path):
            for line in open(directory_path+"/"+file_path).read().split('\n')[:-1]:
                self.add_document(line)
        self.index_writer.commit()

    def search(self, query):
        #self.message(u"Searching for: \"{}\".".format(query))
        parser = QueryParser(self.default_field, self.schema)
        parsed_query = parser.parse(query)
        return self.searcher.search(parsed_query)


    def get_term_vector(self, term, field):
        return [p for p in self.searcher.postings(field, term).items_as("positions")]

    def get_std_vector(self, terms, field):
        terms = terms.split(' ')
        vectors = [self.get_term_vector(term, field) for term in terms]
        std_vectors = [get_standard_vector(v) for v in vectors]
        return get_standard_vectors_union(std_vectors)

    def get_vector(self, terms, field=None):
        if field == None:
            field = self.default_field

        terms = terms.split(' ')
        vectors = [self.get_term_vector(term, field) for term in terms]
        vector_union = vector.get_vector_union(vectors)
        merged_vector = vector.get_vector_merge(vector_union)
        full_vector = vector.get_full_vector(merged_vector, self.get_count())
        return full_vector

    def get_count(self):
        return self.searcher.doc_count_all()

    def print_search(self, query):
        query_unicode = query.decode('utf-8')
        result = self.search(query_unicode)
        self.message("Found {} results for this query.".format(str(len(result))))
        for r in result:
            data = []
            for field in self.fields:
                data.append(field+":"+r[field])
        print "\t".join(data)

    def print_document(self, index):
        print self.searcher.document()


        data = []
        for field in self.fields:
            data.append(field+":"+result[field])
        print "\t".join(data)


if __name__ == "__main__":
    input_parser = argparse.ArgumentParser()
    input_parser.add_argument('-c', '--create',  help="If you are creating index, please provide path to schema file.")
    input_parser.add_argument('-i', '--index',  help="Path to index directory.", required=True)
    input_parser.add_argument('-af', '--add_file',  help="Path to document to add.")
    input_parser.add_argument('-ad', '--add_directory',  help="Path to directory to add.")
    input_parser.add_argument('-s', '--search',  help="Search results for given query.")
    input_parser.add_argument('-q', '--quiet', action="store_true", help="Show logs to stderr.")
    input_parser.add_argument('-v', '--vector', help="Show vector for given terms.")
    input_parser.add_argument('-d', '--document', help="Print document of given index.")

    args = input_parser.parse_args()
    input_verbose = True
    if args.quiet:
        input_verbose = False
    manager = SearchManager(args.index, args.create, input_verbose)
    if args.add_file:
        manager.add_file(args.add_file)
    if args.add_directory:
        manager.add_directory(args.add_directory)
    if args.search:
        manager.print_search(args.search)
    if args.vector:
        print manager.get_vector(args.vector)
    if args.document:
        print manager.print_document(args.document)

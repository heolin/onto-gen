#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------

import sys

import argparse

from prim import prim
from search_manager import SearchManager
from find_root import get_root
#from vector import get_cosine_dictance
import vector

def message(*arguments):
    sys.stderr.write("[ONTOLOGY GENERATOR]: " +' '.join(map(str, arguments)) + '\n')

class OntologyGenerator(object):
    search_engine = None
    terms = []
    terms_dict = {}
    simmilarity_matrix = []
    spanning_tree = []
    root_node = None

    def __init__(self, index_path, terms=[]):
        self.search_engine = SearchManager(index_path, None)
        self.terms = terms
        self.terms_dict = {}
        self.simmilarity_matrix = []
        self.spanning_tree = []
        self.root_node  = None
        self.update()

    def update(self):
        self.set_matrix()
        self.create_tree()

    def set_matrix(self):
        message("Setting up terms matrix.")
        for t1 in xrange(len(self.terms)):
            term1 = self.terms[t1]
            self.terms_dict[term1] = term1
            self.simmilarity_matrix.append([])

            for t2 in xrange(len(self.terms)):
                term2 = self.terms[t2]
                self.terms_dict[term2] = term2
                term1_vector = self.search_engine.get_vector(term1)
                term2_vector = self.search_engine.get_vector(term2)
                #simmilarity = get_cosine_dictance(term1_vector, term2_vector)
                simmilarity = vector.get_cityblock_dictance(term1_vector, term2_vector)
                max_simmilarity = 32000
                if term1 == term2:
                    simmilarity = max_simmilarity
                self.simmilarity_matrix[t1].append(float(max_simmilarity-simmilarity)/(float(max_simmilarity)))
        message("Terms matrix created.")


    def create_tree(self):
        message("Creating spanning tree.")
        verts = range(len(self.terms))
        self.spanning_tree = prim(verts, self.simmilarity_matrix, 0)
        self.root_node = get_root(self.spanning_tree, verts)

    def print_spanning_tree(self):
        text = "SPANNING TREE:\n"
        text += str(self.spanning_tree)
        return text

    def print_matrix(self):
        text = "SIMMILRITY_MATRIX:"
        text += "\t".join(["term"+str(x) for x in xrange(len(self.terms))]) + '\n'
        for row in self.simmilarity_matrix:
            text += "\t".join([str(round(x, 2)) for x in row]) + '\n'
        return text

    def save_trutle(self, file_path):
        output_file = open(file_path, "w")
        result_text = """

@prefix : <http://www.semanticweb.org/heolin123/ontologies/2014/5/untitled-ontology-9#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://www.semanticweb.org/heolin123/ontologies/2014/5/untitled-ontology-9text<http://www.semanticweb.org/heolin123/ontologies/2014/5/untitled-ontology-9> rdf:type owl:Ontology .

"""

        result_text += ":{0} rdf:type owl:Class .\n".format(self.terms[self.root_node])

        for term_id in xrange(len(self.terms)):
            if term_id == self.root_node:
                continue
            father_id = self.spanning_tree[term_id]
            #print term_id
            #print father_id
            if father_id != None:
                result_text += u":{0} rdf:type owl:Class ;\n\trdfs:subClassOf :{1} .\n\n".format(self.terms[term_id].replace(' ', '_'), self.terms[father_id].replace(' ', '_'))

        output_file.write(result_text.encode('utf-8'))
        output_file.close()




def main():
    input_parser = argparse.ArgumentParser()
    input_parser.add_argument('-i', '--index',  help="Path to index directory.", required=True)
    input_parser.add_argument('-t', '--terms',  help="Path to file with terms.", required=True)
    input_parser.add_argument('-o', '--out',  help="Path to output_file.", required=True)
    input_parser.add_argument('-l', '--log',  help="Path to log file.")


    args = input_parser.parse_args()

    terms = [term.strip() for term in open(args.terms).read().decode('utf-8').split('\n')[:-1]]

    generator = OntologyGenerator(args.index, terms)

    if args.log:
        log_file = open(args.log, 'w')
        log_file.write(generator.print_matrix() + '\n')
        log_file.write(generator.print_spanning_tree() + '\n')
        log_file.close()

    generator.save_trutle(args.out)

if __name__ == "__main__":
    main()

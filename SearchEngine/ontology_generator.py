#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------

import math
import sys

from prim import prim
from create_index import SearchEngine
from find_root import get_root

class OntologyGenerator(object):
    search_engine = None
    terms = []
    terms_dict = {}
    simmilarity_matrix = []
    spanning_tree = []
    root_node = None

    def __init__(self, search_json, terms=[]):
        self.search_engine = SearchEngine.from_json(search_json)
        self.terms = terms
        self.terms_dict = {}
        self.simmilarity_matrix = []
        self.spanning_tree = []
        self.root_node  = None
        self.update()

    def add_term(self, term):
        self.terms.append(term)


    def update(self):
        self.set_matrix()
        self.create_tree()

    def set_matrix(self):
        for t1 in xrange(len(self.terms)):
            term1 = self.terms[t1]
            self.terms_dict[term1] = term1
            self.simmilarity_matrix.append([])

            for t2 in xrange(len(self.terms)):
                term2 = self.terms[t2]
                self.terms_dict[term2] = term2
                simmilarity = self.search_engine.get_cosine_simmilarity(term1, term2)
                if term1 == term2:
                    simmilarity = 1.0
                self.simmilarity_matrix[t1].append(1-simmilarity)


    def create_tree(self):
        verts = range(len(self.terms))
        self.spanning_tree = prim(verts, self.simmilarity_matrix, 0)
        self.root_node = get_root(self.spanning_tree, verts)
        print self.spanning_tree

    def print_matrix(self):
        print "\t".join(["term"+str(x) for x in xrange(len(self.terms))])
        for row in self.simmilarity_matrix:
            print "\t".join([str(round(x,2)) for x in row])

    def save_trutle(self, file_path):
        output_file = open(file_path, "w")
        result_text = """

@prefix : <http://www.semanticweb.org/heolin123/ontologies/2014/5/untitled-ontology-9#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://www.semanticweb.org/heolin123/ontologies/2014/5/untitled-ontology-9> .

<http://www.semanticweb.org/heolin123/ontologies/2014/5/untitled-ontology-9> rdf:type owl:Ontology .

"""

        result_text += ":{0} rdf:type owl:Class .\n".format(self.terms[self.root_node])

        for term_id in xrange(len(self.terms)):
            if term_id == self.root_node:
                continue
            father_id = self.spanning_tree[term_id]
            print term_id
            print father_id
            if father_id != None:
                result_text += u":{0} rdf:type owl:Class ;\n\trdfs:subClassOf :{1} .\n\n".format(self.terms[term_id], self.terms[father_id])

        output_file.write(result_text.encode('utf-8'))
        output_file.close()




def main():
    terms = [term.strip() for term in open(sys.argv[2]).read().decode('utf-8').split(',')]
    generator = OntologyGenerator(sys.argv[1], terms)
    generator.print_matrix()

    generator.save_trutle(sys.argv[3])

if __name__ == "__main__":
    main()

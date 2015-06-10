#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------

import sys
import os
import argparse

from search import search_manager, vector
from topics import topics_manager
from graph import graph, tree
from ontology import ontology
from lang import lemmatize
from test import test

TERM_VECTORS_PATH = "temp/_temp_term.vect"
DISTANCE_PATH = "temp/_temp_{}.dist"

COSINE_DISTANCE_PATH = DISTANCE_PATH.format("cosine_distance")
LSI_DISTANCE_PATH = DISTANCE_PATH.format("lsi_distance")

#przeniesc ontology do graph, a osobno zrobic ontology gdzie elementy sa drzewem skierowanym a nie grafem
def message(*arguments):
    sys.stderr.write("[ONTOLOGY GENERATOR]: " +' '.join(map(str, arguments)) + '\n')


def read_terms(path):
    """Reading terms form input file."""
    return filter(None, [term.strip() for term in open(path).read().decode('utf-8').split('\n')[:-1]])


def get_lemmas(terms):
    """Getting lemmas for each term."""
    lemmas = [lemmatize.process(term) for term in terms]
    return lemmas


def add_terms(ontology_graph, terms, lemmas):
    """Adding terms in Node form into ontology."""
    for term, lemma in zip(terms, lemmas):
        ontology_graph.add_term(term.encode('utf-8'), lemma)
    return ontology_graph


def add_connections(ontology_graph):
    """Adding connections from each node to all others."""
    terms = ontology_graph.terms.values()
    for t1 in xrange(len(terms)):
        for t2 in range(t1 + 1, len(terms)):
            if t1 != t2:
                ontology_graph.add_connection(terms[t1], terms[t2])
    return ontology_graph


def read_distances_map(path):
    result = {}

    if not os.path.isfile(path):
        return result

    for line in [l.split('\t') for l in open(path).read().split('\n')[:-1]]:
        result.setdefault(line[0], {})
        result[line[0]][line[1]] = float(line[2])
    return result


def save_distance(term1, term2, distance, value):
    output_file = open(DISTANCE_PATH.format(distance), "a")
    line = "{}\t{}\t{}\n".format(term1, term2, value)
    output_file.write(line)
    output_file.close()


def save_term_vectors(term_vectors):
    output_file = open(TERM_VECTORS_PATH, "w")
    for key in term_vectors:
        output_file.write(key+"\t")
        output_file.write("\t".join([str(x) for x in term_vectors[key]]))
    output_file.close()


def load_term_vectors():
    if not os.path.isfile(TERM_VECTORS_PATH):
        return None
    print "[LOG]: Loading term vectors."
    vectors = {}
    for line in [t.split('\t') for t in open(TERM_VECTORS_PATH).read().split('\n')[:-1]]:
        vectors[line[0]] = line[1:]
    return vectors


def add_distances(ontology_graph, search_engine, topics):
    """Adding distances to connections."""

    distances_map = {}
    distances_map["cosine_distance"] = read_distances_map(COSINE_DISTANCE_PATH)
    distances_map["lsi_distance"] = read_distances_map(LSI_DISTANCE_PATH)

    print "[LOG]: Creating term vector started."
    terms = ontology_graph.terms.values()

    term_vectors = load_term_vectors()
    if not term_vectors:
        term_vectors = dict(zip(ontology_graph.terms.keys(), [search_engine.get_vector(t.lemma) for t in terms]))
        save_term_vectors(term_vectors)
        print "[LOG]: Saving term vectors"

    print "[LOG]: Creating term vector finished."
    for t1 in xrange(len(terms)):
        #print "{}/{}".format(t1, len(terms))
        for t2 in range(t1 + 1, len(terms)):
            if t1 != t2:
                add_distance(ontology_graph, terms[t1], terms[t2], term_vectors, topics, distances_map)


def add_distance(ontology_graph, term1, term2, term_vectors, topics, distances_map):
    """Adding distance between two terms."""

    vector1 = term_vectors[term1.term]
    vector2 = term_vectors[term2.term]

    cosine_distance = None
    lsi_distance = None
    if term1.term in distances_map["cosine_distance"]:
        if term2.term in distances_map["cosine_distance"][term1.term]:
            cosine_distance = distances_map["cosine_distance"][term1.term][term2.term]
            lsi_distance = distances_map["lsi_distance"][term1.term][term2.term]

    if not cosine_distance:
        cosine_distance = vector.get_cosine_dictance(vector1, vector2)
        lsi_distance = 1 - topics.get_similarity(term1.term, term2.term)

        save_distance(term1.term, term2.term, "cosine_distance", cosine_distance)
        #save_distance(term1.term, term2.term, "lsi_distance", lsi_distance)

    ontology_graph.add_distance(term1, term2, "cosine_distance", cosine_distance)
    ontology_graph.add_distance(term1, term2, 'lsi', lsi_distance)



def create(index_dir, corpus_path, terms_path, lemmatize, output_path, connections):
    """Main creating method."""
    search_engine = search_manager.SearchManager(index_dir, None)
    topics = topics_manager.TopicsManager(corpus_path)

    ontology_graph = graph.Graph()

    print "[LOG]: Reading terms started"
    terms = read_terms(terms_path)
    print "[LOG]: Reading terms finished"
    lemmas = terms
    if lemmatize:
        print "[LOG]: Terms lemmatization started."
        lemmas = get_lemmas(terms)
        print "[LOG]: Terms lemmatization finished."


    print "[LOG]: Adding terms started."
    add_terms(ontology_graph, terms, lemmas)
    print "[LOG]: Adding terms finished."

    print "[LOG]: Adding connections started."
    add_connections(ontology_graph)
    print "[LOG]: Adding connections finished."

    print "[LOG]: Adding distances started."
    add_distances(ontology_graph, search_engine, topics)
    print "[LOG]: Adding distances finished."

    new_graph = graph.Graph()
    for conn in connections:
        if conn[0] not in ontology_graph.terms:
            continue
        if conn[1] not in ontology_graph.terms:
            continue
        new_graph.add_connection(ontology_graph.terms[conn[0]], ontology_graph.terms[conn[1]])
    ontology_tree = tree.convertToTree(ontology_graph.connections, new_graph)

    if output_path:
        ontology.save_trutle(output_path, ontology_tree)

    return new_graph

def main():
    input_parser = argparse.ArgumentParser()
    input_parser.add_argument('-i', '--index',  help="Path to index directory.", required=True)
    input_parser.add_argument('-c', '--corpus',  help="Path to corpus directory.", required=True)
    input_parser.add_argument('-t', '--terms',  help="Path to file with terms.", required=True)
    input_parser.add_argument('-o', '--out',  help="Path to output_file.")
    input_parser.add_argument('-d', '--debug',  help="Path to log file.")
    input_parser.add_argument('-l', '--lemma',  help="Lemmatize terms.")
    input_parser.add_argument('-g', '--input_graph',  help="Path to log file.")

    args = input_parser.parse_args()

    connections = []
    if args.input_graph:
        print "[LOG]: Reusing existing ontology from file: {}.".format(args.input_graph)
        connections = ontology.from_trutle(args.input_graph)
        print "[LOG]: Found {} connections.".format(len(connections))

    result = create(args.index, args.corpus, args.terms, args.lemma, args.out, connections)
    test.test_graph(result)

    #generator.save_trutle(args.out)


if __name__ == "__main__":
    main()

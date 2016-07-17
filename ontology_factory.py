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
from random import random
from word2vec_wrapper import get_word2vec_similarity

TERM_VECTORS_PATH = "temp/_temp_term.vect"
DISTANCE_PATH = "temp/_temp_{}.dist"

COSINE_DISTANCE_PATH = DISTANCE_PATH.format("cosine_distance")
CITYBLOCK_DISTANCE_PATH = DISTANCE_PATH.format("cityblock_distance")
CORRELATION_DISTANCE_PATH = DISTANCE_PATH.format("correlation_distance")
CANBERRA_DISTANCE_PATH = DISTANCE_PATH.format("canberra_dictance")
EUCLIDEAN_DISTANCE_PATH = DISTANCE_PATH.format("euclidean_dictance")
BRAYCURTIS_DISTANCE_PATH = DISTANCE_PATH.format("braycurtis_dictance")
LSI_DISTANCE_PATH = DISTANCE_PATH.format("lsi_distance")
W2V_DISTANCE_PATH = DISTANCE_PATH.format("w2v_distance")

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
        output_file.write("\n")
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
    #Currently using this bad solution.
    #If you want to use different distance functions, uncomment those you want.
    #Reasult will be taken as average of all of them.
    #distances_map["cosine_distance"] = read_distances_map(COSINE_DISTANCE_PATH)
    #distances_map["cityblock_distance"] = read_distances_map(CITYBLOCK_DISTANCE_PATH)
    #distances_map["correlation_distance"] = read_distances_map(CORRELATION_DISTANCE_PATH)
    #distances_map["canberra_dictance"] = read_distances_map(CANBERRA_DISTANCE_PATH)
    #distances_map["euclidean_dictance"] = read_distances_map(EUCLIDEAN_DISTANCE_PATH)
    #distances_map["braycurtis_dictance"] = read_distances_map(BRAYCURTIS_DISTANCE_PATH)
    #distances_map["lsi_distance"] = read_distances_map(LSI_DISTANCE_PATH)
    distances_map["w2v_distance"] = read_distances_map(W2V_DISTANCE_PATH)

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

    distances = {}
    for distance in distances_map:
        if term1.term in distances_map[distance]:
            if term2.term in distances_map[distance][term1.term]:
                distances[distance] = distances_map[distance][term1.term][term2.term]
        if distance not in distances:
            if distance == "cosine_distance":
                distances[distance] = vector.get_cosine_dictance(vector1, vector2)
            if distance == "cityblock_distance":
                distances[distance] = vector.get_cityblock_dictance(vector1, vector2)
            if distance == "correlation_distance":
                distances[distance] = vector.get_correlation_dictance(vector1, vector2)
            if distance == "canberra_dictance":
                distances[distance] = vector.get_canberra_dictance(vector1, vector2)
            if distance == "euclidean_dictance":
                distances[distance] = vector.get_euclidean_dictance(vector1, vector2)
            if distance == "braycurtis_dictance":
                distances[distance] = vector.get_braycurtis_dictance(vector1, vector2)
            if distance == "lsi_distance":
                distances[distance] = 1 - topics.get_similarity(term1.term, term2.term)
            if distance == "w2v_distance":
                distances[distance] = get_word2vec_similarity(term1.term, term2.term)
            save_distance(term1.term, term2.term, distance, distances[distance])

    for distance in distances:
        ontology_graph.add_distance(term1, term2, distance, distances[distance])



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
    input_parser.add_argument('-l', '--lemma', action="store_true", help="Lemmatize terms.")
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

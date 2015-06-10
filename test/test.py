#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
import argparse
from graph import graph
from ontology import ontology

def test_graph(graph):
    max_value = test_max(graph)
    min_value = test_min(graph)
    average = test_average(graph)
    #mean2root = mean_to_root(graph)
    momentum = test_momentum(graph)
    print average
    print max_value
    print min_value


def test_momentum(graph):
    result = 0
    print len(graph.terms.values())
    for node in graph.terms.values():
        print node


def test_average(graph):
    return float(sum([conn.get_distance() for conn in graph.connections])) / float(len(graph.connections))

def test_max(graph):
    return max([conn.get_distance() for conn in graph.connections])

def test_min(graph):
    return min([conn.get_distance() for conn in graph.connections])


##def mean_to_root(graph):
#    mean_to_root_step(graph, graph.root, [graph.root], [])

#def mean_to_root_step(graph, term, history, conns):
#    result = []
#    new_conns = []
#    new_conns.extend(conns)
#    for next_term in graph.connections_dict[term]:
#        if next_term in history:
#      #      continue
#      #  
#        history.append(next_term)

def add_terms(ontology_graph, terms, lemmas):
    """Adding terms in Node form into ontology."""
    for term, lemma in zip(terms, lemmas):
        ontology_graph.add_term(term.encode('utf-8'), lemma)
    return ontology_graph

def create(terms, connections):
    """Main creating method."""
    ontology_graph = graph.Graph()

    print "[LOG]: Adding terms started."
    add_terms(ontology_graph, terms, terms)
    print "[LOG]: Adding terms finished."

    for conn in connections:
        if conn[0] not in ontology_graph.terms:
            continue
        if conn[1] not in ontology_graph.terms:
            continue
        ontology_graph.add_connection(ontology_graph.terms[conn[0]], ontology_graph.terms[conn[1]])
    return ontology_graph


def main():
    input_parser = argparse.ArgumentParser()
    input_parser.add_argument('-g', '--input_graph',  help="Path to log file.")

    args = input_parser.parse_args()

    connections = []
    if args.input_graph:
        print "[LOG]: Reusing existing ontology from file: {}.".format(args.input_graph)
        connections = ontology.from_trutle(args.input_graph)
        terms = set()
        for conn in connections:
            terms.add(conn[0].decode('utf-8'))
            terms.add(conn[1].decode('utf-8'))
        terms = list(terms)
        print connections
        print "[LOG]: Found {} connections.".format(len(connections))
        print "[LOG]: Found {} terms.".format(len(terms))

    new_graph = create(terms, connections)
    test_graph(new_graph)


if __name__ == "__main__":
    main()

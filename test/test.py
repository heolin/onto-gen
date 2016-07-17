#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
import argparse
from graph import graph
from ontology import ontology
from wordnet_test import test_similarity
from testcase_test import testcase_similarity_bad, testcase_similarity_good, testcase_similarity_best
from test_consistency import print_consistency

def test_graph(graph):
    max_value = test_max(graph)
    min_value = test_min(graph)
    average = test_average(graph)
    momentum = test_momentum(graph)
    mean2root = test_mean_to_root(graph)
    mean2grand = test_mean_to_grand(graph)
    linear = test_linear(graph)
    exponential = test_exponential(graph)
    simmilarity = test_similarity(graph)
    testcase_best = testcase_similarity_best(graph)
    testcase_good = testcase_similarity_good(graph)
    testcase_bad = testcase_similarity_bad(graph)

    #print_consistency(graph)

    print "average\t{}".format(average)
    print "max_value\t{}".format(max_value)
    print "min_value\t{}".format(min_value)
    print "momentum\t{}".format(momentum)
    print "mean2root\t{}".format(mean2root)
    print "mean2grand\t{}".format(mean2grand)
    print "linear\t{}".format(linear)
    print "exponential\t{}".format(exponential)
    print "simmilarity\t{}".format(simmilarity)
    print "testcase_best\t{}".format(testcase_best)
    print "testcase_good\t{}".format(testcase_good)
    print "testcase_bad\t{}".format(testcase_bad)


def average(values):
    if len(values) == 0:
        return 0.0
    return sum(values) / float(len(values))

def test_momentum(graph):
    result = 0
    for node in graph.terms.values():
        values = []
        parent_value = None
        if node.parent:
            parent_value = node.parent[1].get_distance()
        for child in node.children:
            node_value = child[1].get_distance()

            if parent_value:
                values.append(average([parent_value, node_value]))
            else:
                values.append(node_value)
        result += average(values)
    return result

def test_mean_to_root(graph):
    result = 0
    for node in graph.terms.values():
        values = []
        current = node.parent
        while current:
            values.append(current[1].get_distance())
            current = current[0].parent
        result += average(values)
    return result

def test_mean_to_grand(graph):
    result = 0
    for node in graph.terms.values():
        values = []
        if node.parent:
            values.append(node.parent[1].get_distance())
            if node.parent[0].parent:
                values.append(node.parent[0].parent[1].get_distance())
        result += average(values)
    return result

def test_linear(graph):
    result = 0
    for node in graph.terms.values():
        values = []
        current = node.parent
        while current:
            values.append(current[1].get_distance())
            current = current[0].parent
        result += weighted_distance(values, range(len(values), 0, -1))
    return result

def test_exponential(graph):
    result = 0
    for node in graph.terms.values():
        values = []
        current = node.parent
        while current:
            values.append(current[1].get_distance())
            current = current[0].parent
        result += weighted_distance(values, map(lambda x: x*x, range(len(values), 0, -1)))
    return result

def weighted_distance(values, weights):
    if len(values) == 0:
        return 0
    return sum([x[0] * x[1] for x in zip(values, weights)]) / float(sum(weights))

def test_average(graph):
    return float(sum([conn.get_distance() for conn in graph.connections])) / float(len(graph.connections))

def test_max(graph):
    return max([conn.get_distance() for conn in graph.connections])

def test_min(graph):
    return min([conn.get_distance() for conn in graph.connections])

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

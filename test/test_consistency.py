#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
from graph import graph, tree
from nltk.corpus import wordnet as ns
import itertools
from nltk.corpus import wordnet as wn

from scipy.stats.stats import pearsonr
import numpy


def print_consistency(graph):
    graph_values = []
    wordnet_values = []
    terms = get_terms(graph)
    for term1 in terms:
        for term2 in terms:
            if term1 == term2:
                continue
            graph_sim = get_graph_similarity(graph, term1, term2)
            print "{}\t{}\t{}".format(term1, term2, graph_sim)

def get_graph_similarity(graph, term1, term2):
    paths = tree.get_shortest_path(term1, term2, graph)
    pairs = [(paths[i], paths[i+1]) for i in xrange(len(paths)-1)]
    connections = [get_connection(graph, t[0], t[1]).get_distance() for t in pairs]
    return sum(connections) / float(len(graph.connections))

def get_connection(graph, term1, term2):
    if term1 not in graph.connections_dict:
        return None
    if term2 not in graph.connections_dict[term1]:
        return None

    conn = graph.connections_dict[term2][term1]
    if not conn:
        conn = graph.connections_dict[term1][term2]
    return conn


def get_wordnet_similarity(worda, wordb):
    wordasynsets = wn.synsets(worda)
    wordbsynsets = wn.synsets(wordb)

    values = []
    for sseta, ssetb in itertools.product(wordasynsets, wordbsynsets):
        pathsim = sseta.path_similarity(ssetb)
        if pathsim != None:
            values.append(pathsim)
    if len(values) == 0:
        return None
    return average(values)


def get_terms(graph):
    terms = set()
    for term1 in graph.connections_dict:
        terms.add(term1)
        for term2 in  graph.connections_dict:
            terms.add(term2)
    return list(terms)


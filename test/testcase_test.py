#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")

from scipy.stats.stats import pearsonr
import numpy
from graph import graph, tree
PATH_GOOD = "test/test_cases_good.tsv"
PATH_BAD = "test/test_cases_bad.tsv"
PATH_BEST = "test/test_cases_best.tsv"



def read_test_cases(path):
    lines = [t.split('\t') for t in open(path).read().split('\n')[:-1]]
    tests = {}
    for l in lines:
        tests.setdefault(l[0], {})
        tests[l[0]][l[1]] = l[2]
    return tests

def get_testcase_similarity(test_cases, term1, term2):
    if term1 in test_cases:
        if term2 in test_cases[term1]:
            return test_cases[term1][term2]

    if term2 in test_cases:
        if term1 in test_cases[term2]:
            return test_cases[term2][term1]
    return None

def testcase_similarity_good(graph):
    return testcase_similarity(graph, PATH_GOOD)

def testcase_similarity_bad(graph):
    return testcase_similarity(graph, PATH_BAD)

def testcase_similarity_best(graph):
    return testcase_similarity(graph, PATH_BEST)

def testcase_similarity(graph, path):
    test_cases = read_test_cases(path)
    graph_values = []
    testcase_values = []
    terms = get_terms(graph)
    for term1 in terms:
        for term2 in terms:
            if term1 == term2:
                continue
            graph_sim = get_graph_similarity(graph, term1, term2)
            testcase_sim = get_testcase_similarity(test_cases, term1, term2)
            if testcase_sim:
                testcase_sim = 5.0 - float(testcase_sim)
                graph_values.append(graph_sim)
                testcase_values.append(testcase_sim)
    per = pearsonr(graph_values, testcase_values)
    return "{}\t{}".format(per[0], per[1])


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


def get_terms(graph):
    terms = set()
    for term1 in graph.connections_dict:
        terms.add(term1)
        for term2 in  graph.connections_dict:
            terms.add(term2)
    return list(terms)


def average(values):
    if len(values) == 0:
        return 0.0
    return sum(values) / float(len(values))

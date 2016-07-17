#!/usr/bin/env python
# -*- coding: utf-8 -*-

from connection import Connection
from graph import Graph
import collections
import itertools

def convertToTree(connections, initial_graph):
    graph = initial_graph
    treeStep(connections, graph)
    graph.root = find_root(graph)
    update_nodes(graph, graph.root, [graph.root])
    return graph


def update_nodes(graph, term1, checked):
    for term2 in graph.connections_dict[term1]:
        if term2 in checked:
            continue
        checked.append(term2)
        graph.terms[term2].parent = (graph.terms[term1], graph.connections_dict[term1][term2])
        graph.terms[term1].add_child(graph.terms[term2], graph.connections_dict[term1][term2])
        update_nodes(graph, term2, checked)




def treeStep(connections, graph):
    connections = clear_connections(connections, graph)
    if len(connections) == 0:
        return graph
    sorted_connections = sorted(connections, key = lambda x: x.get_distance())
    for conn in sorted_connections:
        if conn.first.term in graph.terms or conn.second.term in graph.terms or len(graph.terms) == 0:
            graph.add_connection_ref(conn)
            break
    graph = treeStep(connections, graph)
    return graph


def clear_connections(connections, graph):
    new_connections = []
    for connection in connections:
        if connection.first.term in graph.terms:
            if connection.second.term in graph.terms:
                continue
        new_connections.append(connection)
    return new_connections


def find_root(graph):
    paths = get_all_shortest_paths(graph)
    flatten = list(itertools.chain(*paths))
    counter = collections.Counter(flatten)
    return counter.most_common(1)[0][0]

def get_all_shortest_paths(graph):
    paths = []
    terms = graph.terms.values()
    for t1 in xrange(len(terms)):
        for t2 in range(t1 + 1, len(terms)):
            if t1 != t2:
                paths.append(get_shortest_path(terms[t1].term, terms[t2].term, graph))
    return paths


def get_shortest_path(term1, term2, graph):
    return get_shortest_path_step(term1, term2, graph, [term1])

def get_shortest_path_step(term1, term2, graph, path):
    if term1 == term2:
        return path

    result = None
    for next_term in graph.connections_dict[term1]:
        if next_term in path:
            continue
        current = get_shortest_path_step(next_term, term2, graph, path + [next_term])
        if current != None:
            result = current
            break
    return result



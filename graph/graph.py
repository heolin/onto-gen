#!/usr/bin/env python
# -*- coding: utf-8 -*-

from node import Node
from connection import Connection

class Graph(object):
    terms = {}
    root = None
    connections = []
    connections_dict = {}

    def __init__(self):
        self.root = None
        self.terms = {}
        self.connections_dict = {}
        self.connections = []

    def add_term(self, term, lemma):
        self.terms[term] = Node(term, lemma)

    def add_connection(self, first, second):
        connection = Connection(first, second)

        if first.term not in self.connections_dict:
            self.connections_dict[first.term] = {}
        self.connections_dict[first.term][second.term] = connection

        if second.term not in self.connections_dict:
            self.connections_dict[second.term] = {}
        self.connections_dict[second.term][first.term] = connection

        self.connections.append(connection)

    def add_connection_ref(self, connection):
        if connection.first.term not in self.connections_dict:
            self.connections_dict[connection.first.term] = {}
        self.connections_dict[connection.first.term][connection.second.term] = connection

        if connection.second.term not in self.connections_dict:
            self.connections_dict[connection.second.term] = {}
        self.connections_dict[connection.second.term][connection.first.term] = connection

        if connection.first.term not in self.terms:
            self.terms[connection.first.term] = connection.first

        if connection.second.term not in self.terms:
            self.terms[connection.second.term] = connection.second

        self.connections.append(connection)


    def add_distance(self, first, second, metric, distance):
        self.connections_dict[first.term][second.term].add_distance(metric, distance)

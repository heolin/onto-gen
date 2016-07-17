#!/usr/bin/env python
# -*- coding: utf-8 -*-

from connection import Connection

class Node(object):
    term = None
    lemma = None

    def __init__(self, term, lemma):
        self.term = term
        self.lemma = lemma
        self.parent = None
        self.children = []

    def __str__(self):
        return self.term

    def to_string(self):
        return "term: {}, lemma: {}".format(self.term, self.lemma)

    def add_child(self, child, connection):
        self.children.append((child, connection))

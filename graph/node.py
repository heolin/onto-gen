#!/usr/bin/env python
# -*- coding: utf-8 -*-

from connection import Connection

class Node(object):
    term = None
    lemma = None

    parent = None
    children = []

    def __init__(self, term, lemma):
        self.term = term
        self.lemma = lemma

    def __str__(self):
        return self.term

    def to_string(self):
        return "term: {}, lemma: {}".format(self.term, self.lemma)

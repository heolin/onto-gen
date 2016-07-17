#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Connection(object):
    first = None
    second = None
    distances = {}

    def __init__(self, first, second):
        self.first = first
        self.second = second
        self.distances = {}

    def add_distance(self, metric, distance):
        self.distances[metric] = distance

    def get_distance(self):
        #return self.distances['cosine_distance']
        return average(self.distances.values())

    def __str__(self):
        dist = ["{}:{}".format(k, v) for k, v in self.distances.items()]
        return "{} -> {}, [{}]".format(self.first, self.second, ", ".join(dist))


def average(values):
    if len(values) == 0:
        return 0.0
    return sum(values) / float(len(values))



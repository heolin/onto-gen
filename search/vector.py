#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from scipy.spatial.distance import *


def get_vector_union(vectors):
    union_dict = {}
    for vector in vectors:
        for doc in vector:
            if doc[0] not in union_dict:
                union_dict[doc[0]] = []
            union_dict[doc[0]].append(doc[1])
    result = []
    for key in union_dict:
        if len(union_dict[key]) == len(vectors):
            result.append((key, union_dict[key]))
    return result

def get_vector_merge(vector):
    result = []
    for doc in vector:
        data = doc[1]
        lines = []
        for index in data[0]:
            get_merge_line(index, data[1:], [index], lines)
        if len(lines) > 0:
            result.append((doc[0], len(lines)))
    return result

def get_merge_line(index, data, line, lines):
    if data == []:
        lines.append(line)
        return True

    for term in data[0]:
        if term == index + 1:
            line.append(term)
            return get_merge_line(term, data[1:], line, lines)
    return False

def get_full_vector(input_vector, size):
    result = [0 for _ in xrange(size)]
    for x in input_vector:
        result[x[0]] = x[1]
    return result

def get_standard_vector(position_vector):
    return set([v[0] for v in position_vector])

def get_standard_vectors_union(vectors):
    if len(vectors) == 1:
        return vectors[0]
    elif len(vectors) == 2:
        return vectors[0] & vectors[1]
    else:
        half = int(len(vectors) / 2)
        return get_standard_vectors_union(vectors[:half]) & get_standard_vectors_union(vectors[half:])

def get_standard_full_vector(input_vector, size):
    result = [0 for _ in xrange(size)]
    for x in input_vector:
        result[x] = 1
    return result

def get_braycurtis_dictance(vector1, vector2):
    return braycurtis(vector1, vector2)

def get_canberra_dictance(vector1, vector2):
    return canberra(vector1, vector2)

def get_cityblock_dictance(vector1, vector2):
    return cityblock(vector1, vector2)

def get_correlation_dictance(vector1, vector2):
    return correlation(vector1, vector2)

def get_cosine_dictance(vector1, vector2):
    return cosine(vector1, vector2)

def get_euclidean_dictance(vector1, vector2):
    return euclidean(vector1, vector2)

def get_sqeuclidean_dictance(vector1, vector2):
    return sqeuclidean(vector1, vector2)

if __name__ == "__main__":
    ala = get_standard_vector([(1L, [4]), (2L, [26]), (3L, [0, 23])])
    kota = get_standard_vector([(1L, [5]), (2L, [5]), (3L, [5])])
    ma = get_standard_vector([(1L, [5]), (2L, [5]), (3L, [5])])
    vectors = [ala, ma, kota]
    print get_standard_vectors_union(vectors)

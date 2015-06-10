#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
import itertools
import math

def get_path_to_root(v, tree):
    index = v
    v_list = []

    while tree[index] != None:
        v_list.append(index)
        index = tree[index]
    v_list.append(index)
    return v_list


def get_shortest_path(v1, v2, tree):
    v1_list = get_path_to_root(v1, tree)
    v2_list = get_path_to_root(v2, tree)

    path = []
    found = False
    for p1 in v1_list:
        path.append(p1)
        for pi2 in xrange(len(v2_list)):
            if p1 == v2_list[pi2]:
                found = True
                for p2 in range(pi2-1, -1, -1):
                    path.append(v2_list[p2])
                break
        if found:
            break
    return path


def get_all_paths(tree, verts):
    paths_list = []
    for i in xrange(len(verts)):
        for j in xrange(len(verts)):
            paths_list.append(get_shortest_path(i ,j, tree))

    return paths_list


def get_root(tree, verts):
    paths_list= get_all_paths(tree, verts)

    frequency_dict = {}
    for v in verts:
        frequency_dict[v] = 0
        for path in paths_list:
            if v in path:
                frequency_dict[v] += 1

    max_value = -1
    max_key = None
    for key, value in frequency_dict.iteritems():
        if value > max_value:
            max_value = value
            max_key = key

    return max_key


def main():
    tree = [None, 4, 1, 4, 0, 0]
    print get_root(tree, [0, 1, 2, 3, 4, 5])

if __name__ == "__main__":
    main()

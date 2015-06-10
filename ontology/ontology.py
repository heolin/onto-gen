#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

def save_trutle(file_path, graph):
    output_file = open(file_path, "w")
    name = "graph"
    result_text = """

@prefix : <http://www.semanticweb.org/heolin123/ontologies/{0}#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://www.semanticweb.org/heolin123/ontologies/{0}> .

<http://www.semanticweb.org/heolin123/ontologies/{0}> rdf:type owl:Ontology .
""".format(name)

    result_text += ":{0} rdf:type owl:Class .\n".format(graph.terms[graph.root].term)
    result_text += get_children_text(graph, graph.root, [graph.root])

    output_file.write(result_text)
    output_file.close()


def get_children_text(graph, term1, checked):
    result_text = ""
    for term2 in graph.connections_dict[term1]:
        if term2 in checked:
            continue
        result_text += ":{0} rdf:type owl:Class ;\n\trdfs:subClassOf :{1} .\n\n".format(term2.replace(' ', '_'), term1.replace(' ', '_'))
        checked.append(term2)
        result_text += get_children_text(graph, term2, checked)
    return result_text


def from_trutle(file_path):
    text = open(file_path).read()
    base = re.findall("@base <([^ >]*)>", text)[0]
    connections = re.findall("\n:([^ ]*) [^ ]* owl:Class ;\n[ ]*\n[ ]*rdfs:subClassOf :([^ ]*) ", text)
    connections = re.findall("\n:([^ ]*) [^ ]* owl:Class ;\n[\t]*rdfs:subClassOf :([^ ]*) ", text)
    #terms = [term.replace(base, "") for term in re.findall("([^ ]*) [^ ]* owl:Class ", text)]
    #terms = [term.replace('#', '').split('\n')[0] for term in terms]

    return connections

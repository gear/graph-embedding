import numpy as np
import networkx as nx
import os
from collections import defaultdict
from utils import get_file

blogcatalog_origin = 'http://socialcomputing.asu.edu/uploads/1283153973/BlogCatalog-dataset.zip'

blogcatalog_edgelist = 'data/edges.csv'
blogcatalog_labels = 'data/group-edges.csv'

def load_graph():
    """Download the Blogcatalog data set if needed and create a NetworkX object.

    Returns:
        graph: networkx.Graph object representing an undirected graph""" 
    path = get_file('BlogCatalog-dataset', blogcatalog_origin, 
                    extract=True, archive_format='zip')
    edgelist_file = os.path.join(path, blogcatalog_edgelist)
    label_file = os.path.join(path, blogcatalog_labels)
    
    graph = nx.read_edgelist(edgelist_file, delimiter=',', nodetype=int)
    
    labels = defaultdict(list)
    with open(label_file, 'r') as f:
        for l in f.readlines():
            node_id, group = _read_label(l)
            labels[node_id].append(group)

    return graph, labels

def _read_label(line_str):
    """Internal function to read a line of group-edges.csv file and
    return two integers for node_id and label_id.

    Arguments:
        line_str: A single line with the format: node_id, group_id

    Returns:
        node_id: An integer indicates the node id
        group_id: An integer indicates the node's group or label
    """
    raw_id, raw_group = line_str.split(',')
    return int(raw_id), int(raw_group)

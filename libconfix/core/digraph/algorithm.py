# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006 Joerg Faschingbauer

# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of the
# License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

from libconfix.core.utils.error import Error

from digraph import DirectedGraph, Edge

import toposort

def reached_from(digraph, entrypoints):

    unique_nodes = set()

    for e in entrypoints:
        for n in toposort.toposort(digraph, e):
            unique_nodes.add(n)

    edges = []
    for tail in unique_nodes:
        for head in digraph.successors(tail):
            edges.append(Edge(tail=tail, head=head))

    return DirectedGraph(nodes=[n for n in unique_nodes], edges=edges)

def subgraph(digraph, nodes):

    """ From digraph, select nodes and remaining edges to form a new
    digraph. Return the new digraph. """

    assert nodes.issubset(digraph.nodes())
    return DirectedGraph(
        nodes=nodes,
        edges=select_containing_edges(nodes=nodes,
                                      edges=digraph.edges()))

def subtract(digraph, nodes):

    """ Subtract nodes from digraph, together with the affected
    edges. Return resulting digraph. """

    remaining_nodes = set(digraph.nodes()) - set(nodes)
    return DirectedGraph(
        nodes=remaining_nodes,
        edges=select_containing_edges(nodes=remaining_nodes,
                                      edges=digraph.edges()))
    
def select_containing_edges(nodes, edges):

    """ From edges, select those whose ends are members of nodes (and
    return them). """

    node_set = set(nodes)
    ret_edges = []

    for e in edges:
        if e.head() in node_set and e.tail() in node_set:
            ret_edges.append(e)
            pass
        pass

    return ret_edges

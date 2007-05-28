# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2007 Joerg Faschingbauer

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

from digraph import DirectedGraph, Edge, EdgeSet

import toposort

def reached_from(digraph, entrypoints):
    nodes = toposort.toposort(digraph, entrypoints)
    edges = []
    for tail in nodes:
        for head in digraph.successors(tail):
            edges.append(Edge(tail=tail, head=head))
            pass
        pass

    return DirectedGraph(nodes=nodes, edges=edges)

def nodes_reached_from_including_entry(digraph, entrypoints):
    """ From digraph, select all nodes that can be reached from one of
    the entrypoints, including the entrypoints. Return type is a set."""
    ret = set()
    for e in entrypoints:
        for n in toposort.toposort(digraph, [e]):
            ret.add(n)
            pass
        pass
    return ret

def nodes_reached_from_excluding_entry(digraph, entrypoints):
    """ From digraph, select all nodes that can be reached from one of
    the entrypoints, excluding the entrypoints. return type is a set."""
    ret = nodes_reached_from_including_entry(digraph, entrypoints)
    for e in entrypoints:
        ret.remove(e)
        pass
    return ret

def subgraph(digraph, nodes):

    """ From digraph, select nodes and remaining edges to form a new
    digraph. Return the new digraph."""

    assert nodes.issubset(digraph.nodes())
    return DirectedGraph(
        nodes=nodes,
        edges=select_containing_edges(nodes=nodes,
                                      edges=digraph.edges()))

def combine_graphs(digraphs):
    """ Combine nodes and edges of all graphs in digraphs and return
    the resulting graph."""
    nodes = set()
    edges = EdgeSet()
    for g in digraphs:
        for n in g.nodes():
            nodes.add(n)
            pass
        for e in g.edges():
            edges.add(e)
            pass
        pass
    return DirectedGraph(nodes=nodes, edges=edges)

def subtract_nodes(digraph, nodes):

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

## def nearest_property(digraph, entrypoint, property):

##     # better to explain that along with the real problem we have:

##     # ordinary linking of C code with libraries involves a
##     # topologically sorted link line (in reverse order). not so with
##     # libtool; libtool requires only those libraries to be specified
##     # that are *directly* required by the C code. it does the
##     # topological sort itself.

##     # originally I thought that would be simple: take the direct
##     # successors in the graph and put them on the link line. what is
##     # not so simple about this is that the direct successors need not
##     # necessarily have libraries - I soon encountered one
##     # constellation where a direct successor only consisted of header
##     # files, and only a successor of this successor happened to have a
##     # library. bad luck.

##     # solution: ignore these non-library nodes: if a successor of a
##     # node N is one such non-library node NL, then cut it out and
##     # instead place edges N->S for all sucessors S of NL.

##     # as for "property": since my neurotic goal is to make everything
##     # as general as possible, I declare to see "having a library" and
##     # "not having a library" as property of a node: "has a property"
##     # and "doesn't have a property".

##     work_graph = digraph

##     nodes_with_property = set()
##     while True:
##         nodes_without_property = set()
##         for succ in work_graph.successors(entrypoint):
##             if property.have(succ):
##                 nodes_with_property.add(succ)
##             else:
##                 nodes_without_property.add(succ)
##                 pass
##             pass

##         if len(nodes_without_property) == 0:
##             return nodes_with_property

##         nodes_reached_from_good_nodes = nodes_reached_from_including_entry(
##             digraph=work_graph,
##             entrypoints=nodes_with_property)

##         # cut edges to and from bad nodes. insert shortcut edges
##         # around them to their successors if the successor is not yet
##         # seen by a good node.

##         # sadly we cannot simply delete edges from a graph. maybe
##         # someday someone will implement that. in the meantime we have
##         # to work around this and be a bit more complicated than
##         # necessary.
##         badedges = set()
##         newedges = set()
##         for badnode in nodes_without_property:
##             # cut in-edge
##             badedges.add(work_graph.find_edge(entrypoint, badnode))
##             for edge in work_graph.out_edges(badnode):
##                 # cut out-edge
##                 badedges.add(edge)
##                 # if the node has a successor that we don't see from a
##                 # good node, then add a shortcut edge to that one.
##                 if edge.head() not in nodes_reached_from_good_nodes:
##                     newedges.add(Edge(entrypoint, edge.head()))
##                     pass
##                 pass
##             pass

##         edges = set()
##         for e in work_graph.edges():
##             if e not in badedges:
##                 edges.add(e)
##                 pass
##             pass
##         edges |= newedges

##         work_graph = DirectedGraph(nodes=work_graph.nodes(), edges=edges)
##         pass
##     pass


def nearest_property(digraph, entrypoint, property):

    # better to explain that along with the real problem we have:

    # ordinary linking of C code with libraries involves a
    # topologically sorted link line (in reverse order). not so with
    # libtool; libtool requires only those libraries to be specified
    # that are *directly* required by the C code. it does the
    # topological sort itself.

    # originally I thought that would be simple: take the direct
    # successors in the graph and put them on the link line. what is
    # not so simple about this is that the direct successors need not
    # necessarily have libraries - I soon encountered one
    # constellation where a direct successor only consisted of header
    # files, and only a successor of this successor happened to have a
    # library. bad luck.

    # solution: ignore these non-library nodes: if a successor of a
    # node N is one such non-library node NL, then cut it out and
    # instead place edges N->S for all sucessors S of NL.

    # as for "property": since my neurotic goal is to make everything
    # as general as possible, I declare to see "having a library" and
    # "not having a library" as property of a node: "has a property"
    # and "doesn't have a property".

    work_graph = reached_from(digraph=digraph, entrypoints=[entrypoint])

    nodes_with_property = set()
    while True:
        nodes_without_property = set()
        for succ in work_graph.successors(entrypoint):
            if property.have(succ):
                nodes_with_property.add(succ)
            else:
                nodes_without_property.add(succ)
                pass
            pass

        if len(nodes_without_property) == 0:
            return nodes_with_property

        nodes_reached_from_good_nodes = nodes_reached_from_including_entry(
            digraph=work_graph,
            entrypoints=nodes_with_property)

        # cut edges to and from bad nodes. insert shortcut edges
        # around them to their successors if the successor is not yet
        # seen by a good node.

        badedges = set()
        newedges = set()
        for badnode in nodes_without_property:
            # cut in-edge
            badedges.add(work_graph.find_edge(entrypoint, badnode))
            for edge in work_graph.out_edges(badnode):
                # cut out-edge
                badedges.add(edge)
                # if the node has a successor that we don't see from a
                # good node, then add a shortcut edge to that one.
                if edge.head() not in nodes_reached_from_good_nodes:
                    newedges.add(Edge(entrypoint, edge.head()))
                    pass
                pass
            pass

        edges = set()
        for e in work_graph.edges():
            if e not in badedges:
                edges.add(e)
                pass
            pass
        edges |= newedges

        work_graph = DirectedGraph(nodes=work_graph.nodes(), edges=edges)
        pass
    pass

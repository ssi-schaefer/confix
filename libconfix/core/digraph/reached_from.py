# Copyright (C) 2005 Salomon Automation

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

from . import toposort
from .digraph import Edge, DirectedGraph

def reached_from(digraph, entrypoints):

    unique_nodes = set()

    for e in entrypoints:
        for n in toposort.toposort(digraph, [e]):
            unique_nodes.add(n)

    edges = []
    for tail in unique_nodes:
        for head in digraph.successors(tail):
            edges.append(Edge(tail=tail, head=head))

    return DirectedGraph(nodes=[n for n in unique_nodes], edges=edges)

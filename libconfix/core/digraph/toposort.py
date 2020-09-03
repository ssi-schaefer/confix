# Copyright (C) 2005 Salomon Automation
# Copyright (C) 2005-2009 Salomon Automation

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

import dfs
import cycle

def toposort(digraph, nodes):
    ret = []
    seen = set()
    for n in nodes:
        for topo_n in toposort_node(digraph=digraph, node=n):
            if topo_n not in seen:
                ret.append(topo_n)
                seen.add(topo_n)
                pass
            pass
        pass
    return ret

def toposort_node(digraph, node):
    v = TopoVisitor()
    try:
        dfs.dfs(digraph=digraph, node=node, visitor=v)
    except cycle.CycleError, error:
        # annotate cycle
        edgelist = []
        for tail, head in [(error.nodelist()[i], error.nodelist()[i+1]) for i in xrange(len(error.nodelist())-1)]:
            edge = digraph.find_edge(tail, head)
            assert edge is not None
            edgelist.append(edge)
            pass
        raise cycle.CycleError(nodelist=error.nodelist(), edgelist=edgelist)
    return v.nodes()

class TopoVisitor:

    WHITE = 0
    GRAY  = 1
    BLACK = 2

    def __init__(self):

        self.colormap_ = {}
        self.topolist_ = []
        self.stack_ = []

    def nodes(self): return self.topolist_

    def enter(self, node):

        color = self.get_node_color_(node)

        if color == TopoVisitor.WHITE:
            self.set_node_color_(node, TopoVisitor.GRAY)
            self.stack_.append(node)
            return True
        if color == TopoVisitor.GRAY:
            for i in reversed(xrange(len(self.stack_))):
                if self.stack_[i] == node:
                    cycle_path = self.stack_[i:] + [node]
                    pass
                pass
            assert len(cycle_path)
            raise cycle.CycleError(nodelist=cycle_path)
        if color == TopoVisitor.BLACK:
            return False

    def leave(self, node):

        self.set_node_color_(node, TopoVisitor.BLACK)
        self.topolist_.append(node)
        self.stack_.pop()

    def get_node_color_(self, node):

        return self.colormap_.get(node, TopoVisitor.WHITE)

    def set_node_color_(self, node, color):

        if color == TopoVisitor.WHITE:
            assert 0, "why would you want to do this?"
        elif color == TopoVisitor.GRAY:
            assert not self.colormap_.has_key(node)
            self.colormap_[node] = TopoVisitor.GRAY
        elif color == TopoVisitor.BLACK:
            assert self.colormap_[node] == TopoVisitor.GRAY
            self.colormap_[node] = TopoVisitor.BLACK

class CycleError:

    def __init__(self, path):

        self.path_ = path

    def path(self): return self.path_

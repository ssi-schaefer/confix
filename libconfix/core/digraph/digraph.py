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

class EdgeFinder(object):

    def __init__(self): pass
    def find_out_edges(self, node): assert 0, 'abstract'
    pass

class DirectedGraph(object):

    def __init__(self, nodes, edges=None, edgefinder=None):

        assert edges is None or edgefinder is None
        assert not (edges is not None and edgefinder is not None)

        self.nodes_ = frozenset(nodes)
        self.edges_ = EdgeSet()
        self.edgefinder_ = edgefinder

        # nodes without a successor
        self.terminators_ = set()

        if edges is not None:
            for e in edges:
                assert e.tail() in self.nodes_
                assert e.head() in self.nodes_
                self.edges_.add(e)
                pass
            pass
        pass
    
    def nodes(self): return self.nodes_

    def edges(self):
        self.complete_edges_()
        return self.edges_

    def find_edge(self, tail, head):
        self.complete_edges_()
        return self.edges_.find_edge(tail, head)

    def successors(self, node):
        return [edge.head() for edge in self.out_edges(node)]
    
    def out_edges(self, node):
        assert node in self.nodes_, str(node)+' not among my nodes: '+str([str(n) for n in self.nodes_])
        if node in self.terminators_:
            return []
        ret = self.edges_.out_edges(node)
        if ret is not None:
            return ret
        if self.edgefinder_ is None:
            self.terminators_.add(node)
            return []
        ret = self.edgefinder_.find_out_edges(node)
        if len(ret) == 0:
            self.terminators_.add(node)
            return []
        for e in ret:
            self.edges_.add(e)
            pass
        return ret

    def complete_edges_(self):
        if self.edgefinder_ is None:
            return
        # perform a full edge scan
        for n in self.nodes_:
            self.out_edges(n)
            pass
        # no need to search for edges anymore after a full scan
        self.edgefinder_ = None
        pass
    pass

class Edge(object):

    def __init__(self, tail, head, annotations=None):
        assert tail is not head
        self.tail_ = tail
        self.head_ = head
        self.annotations_ = annotations
        pass
    def tail(self): return self.tail_
    def head(self): return self.head_
    def annotations(self): return self.annotations_
    pass

class EdgeSet(object):

    def __init__(self, edges=[]):

        self.by_tail_ = {}
        self.by_head_ = {}

        for e in edges:
            self.add(e)
            pass
        pass

    def add(self, edge):
        by_tail = self.by_tail_.get(edge.tail())
        by_head = self.by_head_.get(edge.head())

        if self.find_edge(edge.tail(), edge.head()):
            return
        
        if by_tail is None:
            by_tail = set()
            self.by_tail_[edge.tail()] = by_tail
            pass
        if by_head is None:
            by_head = set()
            self.by_head_[edge.head()] = by_head
            pass
        by_tail.add(edge)
        by_head.add(edge)
        pass

    def out_edges(self, node):
        return self.by_tail_.get(node)

    def find_edge(self, tail, head):
        by_tail = self.by_tail_.get(tail)
        if by_tail is None:
            return None
        by_head = self.by_head_.get(head)
        if by_head is None:
            return None
        found_edges = by_tail & by_head
        if len(found_edges) == 0:
            return None
        assert len(found_edges) == 1
        return found_edges.pop()

    def __iter__(self):
        ret = set()
        for edgeset in self.by_tail_.itervalues():
            ret.update(edgeset)
            pass
        for edgeset in self.by_head_.itervalues():
            ret.update(edgeset)
            pass
        return ret.__iter__()

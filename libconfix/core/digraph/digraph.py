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

class EdgeFinder(object):

    def __init__(self): pass
    def find_out_edges(self, node): assert 0, 'abstract'
    pass

class DirectedGraph(object):

    def __init__(self, nodes, edges=None, edgefinder=None):

        assert edges is None or edgefinder is None
        assert not (edges is not None and edgefinder is not None)

        self.__nodes = frozenset(nodes)
        self.__edges = EdgeSet()
        self.__edgefinder = edgefinder

        # nodes without a successor
        self.terminators_ = set()

        if edges is not None:
            for e in edges:
                assert e.tail() in self.__nodes
                assert e.head() in self.__nodes
                self.__edges.add(e)
                pass
            pass
        pass


    
    def nodes(self): return self.__nodes

    def edges(self):
        self.complete_edges_()
        return self.__edges

    def edgefinder(self):
        return self.__edgefinder

    def find_edge(self, tail, head):
        self.out_edges(tail)
        return self.__edges.find_edge(tail, head)

    def successors(self, node):
        return [edge.head() for edge in self.out_edges(node)]
    
    def out_edges(self, node):
        assert node in self.__nodes, str(node)+' not among my nodes: '+str([str(n) for n in self.__nodes])
        if node in self.terminators_:
            return []
        ret = self.__edges.out_edges(node)
        if ret is not None:
            return ret
        if self.__edgefinder is None:
            self.terminators_.add(node)
            return []
        ret = self.__edgefinder.find_out_edges(node)
        if len(ret) == 0:
            self.terminators_.add(node)
            return []
        for e in ret:
            self.__edges.add(e)
            pass
        return ret

    def complete_edges_(self):
        if self.__edgefinder is None:
            return
        # perform a full edge scan
        for n in self.__nodes:
            self.out_edges(n)
            pass
        # no need to search for edges anymore after a full scan
        self.__edgefinder = None
        pass
    pass

class Edge(object):

    def __init__(self, tail, head, annotations=None):
        assert tail is not head
        self.__tail = tail
        self.__head = head
        self.__annotations = annotations
        pass
    def tail(self): return self.__tail
    def head(self): return self.__head
    def annotations(self): return self.__annotations
    pass

class EdgeSet(object):

    def __init__(self, edges=[]):

        self.__by_tail = {}
        self.__by_head = {}

        for e in edges:
            self.add(e)
            pass
        pass

    def add(self, edge):
        by_tail = self.__by_tail.get(edge.tail())
        by_head = self.__by_head.get(edge.head())

        if self.find_edge(edge.tail(), edge.head()):
            return
        
        if by_tail is None:
            by_tail = set()
            self.__by_tail[edge.tail()] = by_tail
            pass
        if by_head is None:
            by_head = set()
            self.__by_head[edge.head()] = by_head
            pass
        by_tail.add(edge)
        by_head.add(edge)
        pass

    def out_edges(self, node):
        return self.__by_tail.get(node)

    def find_edge(self, tail, head):
        by_tail = self.__by_tail.get(tail)
        if by_tail is None:
            return None
        by_head = self.__by_head.get(head)
        if by_head is None:
            return None
        found_edges = by_tail & by_head
        if len(found_edges) == 0:
            return None
        assert len(found_edges) == 1
        return found_edges.pop()

    def __iter__(self):
        ret = set()
        for edgeset in self.__by_tail.itervalues():
            ret.update(edgeset)
            pass
        for edgeset in self.__by_head.itervalues():
            ret.update(edgeset)
            pass
        return ret.__iter__()

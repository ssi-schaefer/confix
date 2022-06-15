# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2012 Joerg Faschingbauer

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

from libconfix.core.digraph.digraph import DirectedGraph, Edge
from libconfix.core.digraph import algorithm

import unittest

class NodesReachedFromIncludingEntry(unittest.TestCase):
    def test(self):
        n1 = object()
        n2 = object()
        n3 = object()

        digraph = DirectedGraph(nodes=[n1, n2, n3],
                                edges=[Edge(n1, n2),
                                       Edge(n1, n3)])
        self.assertEqual(set([n1, n2, n3]),
                             set(algorithm.nodes_reached_from_including_entry(digraph, entrypoints=[n1])))

        digraph = DirectedGraph(nodes=[n1, n2, n3],
                                edges=[Edge(n1, n2),
                                       Edge(n2, n3)])
        self.assertEqual(set([n1, n2, n3]),
                             set(algorithm.nodes_reached_from_including_entry(digraph, entrypoints=[n1])))

        digraph = DirectedGraph(nodes=[n1, n2, n3],
                                edges=[Edge(n1, n2),
                                       Edge(n2, n3)])
        self.assertEqual(set([n2, n3]),
                             set(algorithm.nodes_reached_from_including_entry(digraph, entrypoints=[n2])))
        pass
    pass

class SubtractNodes(unittest.TestCase):
    def test(self):
        n1 = object()
        n2 = object()
        n3 = object()
        n4 = object()

        digraph = DirectedGraph(nodes=[n1, n2, n3, n4],
                                edges=[Edge(n1, n2),
                                       Edge(n2, n3),
                                       Edge(n3, n4),
                                       Edge(n1, n4)])
        subtracted_digraph = algorithm.subtract_nodes(digraph=digraph, nodes=[n2, n3])
        self.assertEqual(set([n1, n4]),
                             set(subtracted_digraph.nodes()))
        self.assertTrue(subtracted_digraph.find_edge(n1, n4))
        pass
    pass

class CombineGraphs(unittest.TestCase):
    def test(self):
        n1 = object()
        n2 = object()
        n3 = object()
        n4 = object()

        g = algorithm.combine_graphs([DirectedGraph(nodes=[n1, n2, n3],
                                                    edges=[Edge(n1, n2),
                                                           Edge(n1, n3)]),
                                      DirectedGraph(nodes=[n2, n3],
                                                    edges=[Edge(n2, n3)]),
                                      DirectedGraph(nodes=[n3, n4],
                                                    edges=[Edge(n3, n4)]),
                                      DirectedGraph(nodes=[n1, n2],
                                                    edges=[Edge(n1, n2)])])
        self.assertEqual(set([n1, n2, n3, n4]),
                             set(g.nodes()))

        self.assertTrue(g.find_edge(n1, n2))
        self.assertTrue(g.find_edge(n1, n3))
        self.assertTrue(g.find_edge(n2, n3))
        self.assertTrue(g.find_edge(n3, n4))
        pass
    pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(NodesReachedFromIncludingEntry))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SubtractNodes))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(CombineGraphs))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass


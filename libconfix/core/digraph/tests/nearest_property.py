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

import unittest

from libconfix.core.digraph.digraph import DirectedGraph, Edge
from libconfix.core.digraph import algorithm

class Node:
    GOOD = 0
    BAD = 1
    def __init__(self, property):
        assert property in [self.GOOD, self.BAD]
        self.__property = property
        pass
    def property(self):
        return self.__property
    pass

class GoodProperty:
    def have(self, node):
        return node.property() == Node.GOOD
    pass

class NearestProperty(unittest.TestCase):

    # in the pictures below, edges flow from left to right (I don't
    # bother drawing arrow heads in picture mode) unless explicitly
    # given.

    # underlined nodes are those having the property.

    def test0(self):

        # root ---- bad      yields []

        root = Node(Node.BAD)
        bad = Node(Node.BAD)
        digraph = DirectedGraph(nodes=[root, bad],
                                edges=[Edge(root, bad)])
        self.failUnlessEqual(set(),
                             algorithm.nearest_property(digraph=digraph,
                                                        entrypoint=root,
                                                        property=GoodProperty()))
        pass        

    def test1(self):

        #         bad1
        #       /      \
        # root /        good       yields good
        #      \       /----
        #       \     /
        #         bad2

        root = Node(Node.BAD)
        bad1 = Node(Node.BAD)
        bad2 = Node(Node.BAD)
        good = Node(Node.GOOD)

        digraph = DirectedGraph(nodes=[root, bad1, bad2, good],
                                edges=[Edge(tail=root, head=bad1),
                                       Edge(tail=root, head=bad2),
                                       Edge(tail=bad1, head=good),
                                       Edge(tail=bad2, head=good)])

        self.failUnlessEqual(set([good]),
                             algorithm.nearest_property(digraph=digraph,
                                                        entrypoint=root,
                                                        property=GoodProperty()))
        pass

    def test2(self):

        #         bad
        #       /    \
        # root /______\ good    yields good
        #               ----

        root = Node(Node.BAD)
        bad = Node(Node.BAD)
        good = Node(Node.GOOD)

        digraph = DirectedGraph(nodes=[root, bad, good],
                                edges=[Edge(root, bad),
                                       Edge(root, good),
                                       Edge(bad, good)])
        self.failUnlessEqual(set([good]),
                             algorithm.nearest_property(digraph=digraph,
                                                        entrypoint=root,
                                                        property=GoodProperty()))
        pass

    def test3(self):

        #                 good1 --- good3
        #               / -----     -----
        #         bad1 /
        #       /      \             yields good1, good2
        # root /        \ good2
        #      \         /-----
        #       \       /
        #         bad2 /

        root = Node(Node.BAD)
        bad1 = Node(Node.BAD)
        bad2 = Node(Node.BAD)
        good1= Node(Node.GOOD)
        good2= Node(Node.GOOD)
        good3= Node(Node.GOOD)
        digraph = DirectedGraph(nodes=[root, bad1, bad2, good1, good2, good3],
                                edges=[Edge(root, bad1),
                                       Edge(root, bad2),
                                       Edge(bad1, good1),
                                       Edge(bad1, good2),
                                       Edge(bad2, good2),
                                       Edge(good1, good3)])
        self.failUnlessEqual(set([good1, good2]),
                             algorithm.nearest_property(digraph=digraph,
                                                        entrypoint=root,
                                                        property=GoodProperty()))
        pass

    def test4(self):

        #         bad
        #       /      \
        # root /        \  good2      yields good1
        #      \         / -----
        #       \       /
        #         good1
        #         -----

        root = Node(Node.BAD)
        bad = Node(Node.BAD)
        good1 = Node(Node.GOOD)
        good2 = Node(Node.GOOD)
        digraph = DirectedGraph(nodes=[root, bad, good1, good2],
                                edges=[Edge(root, bad),
                                       Edge(bad, good2),
                                       Edge(root, good1),
                                       Edge(good1, good2)])
        self.failUnlessEqual(set([good1]),
                             algorithm.nearest_property(digraph=digraph,
                                                        entrypoint=root,
                                                        property=GoodProperty()))
        pass

    def test5(self):

        #          bad
        #        /     \
        #       /       \
        # root            good2
        #       \         -----      yields good1
        #        \      /
        #          good1
        #          -----

        root = Node(Node.BAD)
        bad = Node(Node.BAD)
        good1 = Node(Node.GOOD)
        good2 = Node(Node.GOOD)
        digraph = DirectedGraph(nodes=[root, bad, good1, good2],
                                edges=[Edge(root, bad),
                                       Edge(root, good1),
                                       Edge(bad, good2),
                                       Edge(good1, good2)])
        self.failUnlessEqual(set([good1]),
                             algorithm.nearest_property(digraph=digraph,
                                                        entrypoint=root,
                                                        property=GoodProperty()))
        pass

    def test6(self):

        #         bad
        #       /     \
        #      /       \
        # root           good2
        #      \         -----     yields good1, good2
        #       \
        #         good1
        #         -----

        root = Node(Node.BAD)
        bad = Node(Node.BAD)
        good1 = Node(Node.GOOD)
        good2 = Node(Node.GOOD)
        digraph = DirectedGraph(nodes=[root, bad, good1, good2],
                                edges=[Edge(root, bad),
                                       Edge(root, good1),
                                       Edge(bad, good2)])
        self.failUnlessEqual(set([good1, good2]),
                            algorithm.nearest_property(digraph=digraph,
                                                       entrypoint=root,
                                                       property=GoodProperty()))
        pass

    def test7(self):

        #          bad
        #        /
        #       /
        #      /
        # root ----------- good1
        #      \           -----     yields good1, good2 (good1 is seen through good2,
        #       \         /          but is a direct successor of root)
        #        \       /
        #          good2
        #          -----

        root = Node(Node.BAD)
        bad = Node(Node.BAD)
        good1 = Node(Node.GOOD)
        good2 = Node(Node.GOOD)
        digraph = DirectedGraph(nodes=[root, bad, good1, good2],
                                edges=[Edge(root, bad),
                                       Edge(root, good1),
                                       Edge(root, good2),
                                       Edge(good2, good1)])
        self.failUnlessEqual(set([good1, good2]),
                             algorithm.nearest_property(digraph=digraph,
                                                        entrypoint=root,
                                                        property=GoodProperty()))
        pass

    def test8(self):


        # root --- good1 --- good2     yields good1

        root = Node(Node.BAD)
        good1 = Node(Node.GOOD)
        good2 = Node(Node.GOOD)
        digraph = DirectedGraph(nodes=[root, good1, good2],
                                edges=[Edge(root, good1),
                                       Edge(good1, good2)])
        self.failUnlessEqual(set([good1]),
                             algorithm.nearest_property(digraph=digraph,
                                                        entrypoint=root,
                                                        property=GoodProperty()))
        pass
    
    pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(NearestProperty))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass

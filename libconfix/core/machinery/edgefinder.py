# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2009 Joerg Faschingbauer

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

from dependency_utils import ProvideMap
from require import Require
from resolve_error import NotResolved

from libconfix.core.utils import debug
from libconfix.core.digraph import digraph
from libconfix.core.utils.error import Error

class EdgeFinder(digraph.EdgeFinder):

    def __init__(self, nodes):
        """
        Find successors of a node by matching that node's require
        objects against the provide objects of all nodes.

        Unresolved require objects are remembered for later use by
        raise_unresolved().
        """

        # we remember require objects that we haven't been able to
        # resolve. list of (require, node).
        self.__unresolved_requires = []

        # index nodes by what they provide, in a fascist manner.
        
        self.__providemap = ProvideMap(permissive=False)
        errors = []
        for n in nodes:
            for p in n.provides():
                try:
                    self.__providemap.add(p, n)
                except Error, e:
                    errors.append(Error('"'+str(p)+'" of node '+str(n), [e]))
                    pass
                pass
            pass
        if len(errors):
            raise Error('Failed making provide-objects public', errors)

        pass

    def find_out_edges(self, node):
        # dictionary:
        #    key: node
        #    value: set of requires that pull in the node
        successors = {}
        
        for r in node.requires():
            found_nodes = self.__providemap.find_match(r)

            if len(found_nodes) == 0:
                self.__unresolved_requires.append((r, node))
                continue
            if len(found_nodes) > 1:
                raise AmbiguouslyResolved(require=r, nodes=found_nodes)
            
            successor = found_nodes[0]
            assert successor is not node, 'self-cycle detected'
            if not successors.has_key(successor):
                successors[successor] = set()
                pass
            successors[successor].add(r)
            pass

        edges = []
        for succ, requires in successors.iteritems():
            edges.append(digraph.Edge(tail=node, head=succ, annotations=requires))
            pass

        return edges

    def raise_unresolved(self):
        error = NotResolved()
        for require, node in self.__unresolved_requires:
            if require.urgency() == Require.URGENCY_ERROR:
                error.add(require, node)
                continue
            if require.urgency() == Require.URGENCY_WARN:
                debug.warn('Require object '+str(require)+' could not be resolved')
                continue
            if require.urgency() == Require.URGENCY_IGNORE:
                continue
            assert 0, 'huh? missed urgency level '+str(require.urgency())
            pass
        if len(error) > 0:
            raise error
        pass

    pass

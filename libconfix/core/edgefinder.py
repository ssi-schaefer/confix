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

from libconfix.core.digraph import digraph
from libconfix.core.utils.error import Error

from depindex import ProvideMap
from require import Require
from libconfix.core.utils import debug

class EdgeFinder(digraph.EdgeFinder):

    class RequireNotResolved(Error):
        def __init__(self, require):
            Error.__init__(self, 'Require object '+str(require)+' could not be resolved')
            self.require_ = require
            pass
        def require(self):
            return self.require_
        pass
    class SuccessorNotFound(Error):
        def __init__(self, node, errors):
            Error.__init__(self, 'Cannot find successors of node '+str(node), errors)
            self.node_ = node
            pass
        def node(self):
            return self.node_
        pass

    def __init__(self, nodes):

        # index nodes by what they provide, in a fascist manner.
        
        self.providemap_ = ProvideMap(permissive=False)
        errors = []
        for n in nodes:
            for p in n.provides():
                try:
                    self.providemap_.add(p, n)
                except Error, e:
                    errors.append(Error('"'+str(p)+'" of node '+str(n), [e]))
                    pass
                pass
            pass
        if len(errors):
            raise Error('Failed making provide-objects public', errors)

        pass

    def find_out_edges(self, node):
        errors = []

        # dictionary:
        #    key: node
        #    value: set of requires that pull in the node
        successors = {}
        
        for r in node.requires():
            found_nodes = self.providemap_.find_match(r)

            if len(found_nodes) == 0:
                if r.urgency() == Require.URGENCY_ERROR:
                    errors.append(EdgeFinder.RequireNotResolved(r))
                    continue
                if r.urgency() == Require.URGENCY_WARN:
                    debug.warn('Require object '+str(r)+' could not be resolved')
                    continue
                if r.urgency() == Require.URGENCY_IGNORE:
                    continue
                assert 0, 'huh? missed urgency level '+str(r.urgency())
                pass
            if len(found_nodes) > 1:
                errors.append(Error('Found more than one node resolving require object "'+\
                                    str(r)+': '+\
                                    str(['.'.join(n.fullname()) for n in found_nodes])))
                continue

            successor = found_nodes[0]
            assert successor is not node, 'self-cycle detected'
            if not successors.has_key(successor):
                successors[successor] = set()
                pass
            successors[successor].add(r)

            pass

        if len(errors):
            raise EdgeFinder.SuccessorNotFound(node, errors)

        edges = []
        for succ, requires in successors.iteritems():
            edges.append(digraph.Edge(tail=node, head=succ, annotations=requires))
            pass

        return edges

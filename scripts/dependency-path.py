#!/usr/bin/env python

# $Id: dependency-path.py,v 1.2 2006/02/06 21:07:42 jfasch Exp $

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

from libconfix.repo_composite import CompositePackageRepository
from libconfix.repo_automake import AutomakePackageRepository
from libconfix.digraph.digraph import DirectedGraph
from libconfix.edgefinder import EdgeFinder
from libconfix.error import Error
from libconfix.digraph.toposort import toposort
from libconfix.digraph.reached_from import reached_from

import sys

def find_paths(graph, from_node, to_node):
    paths = []
    for n in graph.calculate_successors_(from_node):
        if n is to_node:
            paths.append([from_node, to_node])
            pass
        else:
            for path in find_paths(graph, n, to_node):
                paths.append([from_node] + path)
                pass
            pass
        pass
    return paths

repo_dirs = sys.argv[1].split(',')
from_name = sys.argv[2].split('.')
to_name = sys.argv[3].split('.')

try:

    repo = CompositePackageRepository()

    for d in repo_dirs:
        r = AutomakePackageRepository(d)
        repo.add_repo(r)
        pass

    modules = []
    for p in repo.packages():
        modules.extend(p.modules())
        pass

    graph = DirectedGraph(nodes=modules,
                          edgefinder=EdgeFinder(modules=modules))

    from_node = None
    to_node = None
    for n in graph.nodes():
        if n.fullname() == from_name:
            from_node = n
            pass
        if n.fullname() == to_name:
            to_node = n
            pass
        pass

    if from_node is None:
        raise Error('Module '+'.'.join(from_name)+' not found')
    if to_node is None:
        raise Error('Module '+'.'.join(to_name)+' not found')

    print ['.'.join(m.fullname()) for m in reached_from(graph, [from_node]).nodes()]
            
except Error, e:
    sys.stderr.write('***ERROR***\n')
    sys.stderr.write(`e`+'\n')
    sys.exit(1)
    pass


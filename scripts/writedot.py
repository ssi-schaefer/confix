#!/usr/bin/env python

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

import sys

from libconfix.core.utils.error import Error
from libconfix.core.repo.package_file import PackageFile
from libconfix.core.filesys.file import File
from libconfix.core.utils.helper import lines_of_file
from libconfix.core.digraph.digraph import DirectedGraph
from libconfix.core.machinery.edgefinder import EdgeFinder

from libconfix.plugins.automake.helper import automake_name

def write_graph(graph):

    lines = []

    lines.append('digraph my_wonderful_digraph {')

    # create clusters
    clusters = {}
    for n in graph.nodes():
        cluster = clusters.setdefault(n.package(), set())
        cluster.add(n)
        pass

    for package, nodes in clusters.items():
        lines.append('  subgraph cluster_'+automake_name(package.name())+' {')
        for n in nodes:
            lines.append('    '+automake_name('_'.join([package.name()]+n.name()))+\
                         '[label="'+'.'.join([package.name()]+n.name())+'"];')
            pass
        lines.append('  };')
        pass
            
    lines.append('')

    # edges

    for e in graph.edges():
        lines.append('  '+automake_name('_'.join([e.tail().package().name()]+e.tail().name()))+' -> '
                     ''+automake_name('_'.join([e.head().package().name()]+e.head().name()))+';')
        pass

    lines.append('}')

    return lines


def main():
    try:
        nodes = []
        for filename in sys.argv[1:]:
            pkg = PackageFile(File(lines=lines_of_file(filename))).load()
            nodes.extend(pkg.nodes())
            pass
        
        graph = DirectedGraph(nodes=nodes, edgefinder=EdgeFinder(nodes=nodes))
        
        print('\n'.join(write_graph(graph)))

    except Error as e:
        print(repr(e))

if __name__ == "__main__":
    main()



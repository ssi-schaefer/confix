#!/usr/bin/env python

# $Id: find-path.py,v 1.1 2006/03/29 12:19:34 jfasch Exp $

# Copyright (C) 2002-2006 Salomon Automation

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

import libconfix.core.debug
import libconfix.digraph.find_path

import sys, pickle

from_name = sys.argv[1]
to_name = sys.argv[2]

from_list = from_name.split('.')
to_list = to_name.split('.')

digraph = pickle.load(sys.stdin)

from_node = None
to_node = None
for n in digraph.nodes():
    if n.fullname() == from_list:
        from_node = n
        continue
    if n.fullname() == to_list:
        to_node = n
        continue
    pass

if from_node is None:
    libconfix.core.debug.die('Node '+from_name+' not found')
    pass

if to_node is None:
    libconfix.core.debug.die('Node '+to_name+' not found')
    pass

path = libconfix.digraph.find_path.find_path(digraph, from_node, to_node)
for i in xrange(len(path) - 1):
    tail = path[i]
    head = path[i+1]
    print str(tail) + ' -> ' + str(head)
    edge = digraph.find_edge(tail, head)
    assert edge is not None
    for a in edge.annotations():
        print '    '+str(a)
        pass
    pass

# $Id: dfs.py,v 1.1 2006/06/27 15:08:59 jfasch Exp $

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

class Visitor:
    def __init__(self): pass
    def enter(self, node): assert 0
    def leave(self, node): assert 0
    pass

class DefaultVisitor(Visitor):
    def __init__(self):
        Visitor.__init__(self)
        pass
    def enter(self, node): return True
    def leave(self, node): pass
    pass

def dfs(digraph, node, visitor=DefaultVisitor()):
    if not visitor.enter(node):
        return
    for n in digraph.successors(node):
        dfs(digraph, n, visitor)
        pass
    visitor.leave(node)
    pass

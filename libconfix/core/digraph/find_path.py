# $Id: find_path.py,v 1.1 2006/06/27 15:08:59 jfasch Exp $

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

import dfs

def find_path(digraph, from_node, to_node):
    assert from_node in digraph.nodes()
    assert to_node in digraph.nodes()

    visitor = FindPathVisitor(node=to_node)
    dfs.dfs(digraph=digraph, node=from_node, visitor=visitor)
    if visitor.found():
        return visitor.path()
    return []

class FindPathVisitor(dfs.Visitor):
    def __init__(self, node):
        dfs.Visitor.__init__(self)
        self.node_ = node
        self.path_ = []
        self.found_ = False
        pass

    def found(self):
        return self.found_

    def path(self):
        return self.path_

    def enter(self, node):
        if self.found_ == True:
            return False
        self.path_.append(node)
        if node is self.node_:
            self.found_ = True
            return False
        return True

    def leave(self, node):
        if not self.found_:
            self.path_.pop()
            pass
        pass
    
    pass


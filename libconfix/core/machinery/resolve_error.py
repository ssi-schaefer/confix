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

from libconfix.core.utils.error import Error

class NotResolved(Error):
    def __init__(self):
        Error.__init__(self, 'There were require objects that haven\'t been resolved')
        pass
    def add(self, require, node):
        Error.add(self, Error(str(require)+' of node '+str(node)))
        pass
    def __len__(self):
        return len(self.errors())
    pass

class AmbiguouslyResolved(Error):
    def __init__(self, require, nodes):
        Error.__init__(self, 'Require object '+str(require)+' was ambiguously resolved by the following nodes: '+str([str(n) for n in nodes]))
        pass
    pass

class AmbiguouslyProvided(Error):
    def __init__(self, provide, nodes):
        Error.__init__(self, 'Prov object '+str(require)+' was ambiguously resolved by the following nodes: '+str([str(n) for n in nodes]))
        pass
    pass

class SuccessorNotFound(Error):
    def __init__(self, node, errors):
        Error.__init__(self, 'Cannot find successors of node '+str(node), errors)
        self.__node = node
        pass
    def node(self):
        return self.__node
    pass

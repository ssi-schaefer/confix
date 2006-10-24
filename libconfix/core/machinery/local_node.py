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

from node import Node

class LocalNode(Node):
    def get_marshalling_data(self):
        assert 0
        pass
    def set_marshalling_data(self, data):
        assert 0
        pass
    
    def __str__(self):
        return 'LocalNode:'+str(self.responsible_builder_)+', package:'+str(self.responsible_builder_.package())

    def managed_builders(self):
        assert 0
        pass

    def relate_managed_builders(self, digraph):
        assert 0
        pass

    pass

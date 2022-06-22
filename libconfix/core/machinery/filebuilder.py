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

from .entrybuilder import EntryBuilder

from libconfix.core.utils.error import Error
from libconfix.core.machinery.interface import InterfaceProxy

import types

class FileBuilder(EntryBuilder):
    def __init__(self, file):
        EntryBuilder.__init__(self, entry=file)
        pass
    def file(self):
        return self.entry()
    def iface_pieces(self):
        return EntryBuilder.iface_pieces(self) + \
               [FileBuilderInterfaceProxy(builder=self)]
    pass

class FileBuilderInterfaceProxy(InterfaceProxy):
    def __init__(self, builder):
        InterfaceProxy.__init__(self)

        self.__builder = builder

        self.add_global('SET_FILE_PROPERTIES', getattr(self, 'SET_FILE_PROPERTIES'))
        self.add_global('SET_FILE_PROPERTY', getattr(self, 'SET_FILE_PROPERTY'))
        pass

    def SET_FILE_PROPERTIES(self, properties):
        if properties is None:
            raise Error("SET_FILE_PROPERTIES(): 'properties' parameter cannot be None")
        if not type(properties) is dict:
            raise Error("SET_FILE_PROPERTIES(): 'properties' parameter must be a dictionary")
        for name, value in properties.items():
            self.__builder.file().set_property(name=name, value=value)
            # we have modified a property, which at least *might* have
            # influence on the graph
            self.__builder.force_enlarge()
            pass
        pass

    def SET_FILE_PROPERTY(self, name, value):
        if type(name) is not str:
            raise Error("SET_FILE_PROPERTY(): 'name' must be a string")
        self.__builder.file().set_property(name, value)
        # we have modified a property, which at least *might* have
        # influence on the graph
        self.__builder.force_enlarge()
        pass
    
    pass

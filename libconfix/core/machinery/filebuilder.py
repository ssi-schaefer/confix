# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2007 Joerg Faschingbauer

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

import types

from libconfix.core.utils.error import Error
from libconfix.core.iface.proxy import InterfaceProxy

from entrybuilder import EntryBuilder

class FileBuilder(EntryBuilder):
    def __init__(self, file):
        EntryBuilder.__init__(self, entry=file)
        pass
    def file(self):
        return self.entry()
    def iface_pieces(self):
        return EntryBuilder.iface_pieces(self) + \
               [FileBuilderInterfaceProxy(object=self)]
    pass

class FileBuilderInterfaceProxy(InterfaceProxy):
    def __init__(self, object):
        InterfaceProxy.__init__(self, object=object)

        self.add_global('SET_FILE_PROPERTIES', getattr(self, 'SET_FILE_PROPERTIES'))
        self.add_global('SET_FILE_PROPERTY', getattr(self, 'SET_FILE_PROPERTY'))
        pass

    def SET_FILE_PROPERTIES(self, properties):
        if properties is None:
            raise Error("SET_FILE_PROPERTIES(): 'properties' parameter cannot be None")
        if not type(properties) is types.DictionaryType:
            raise Error("SET_FILE_PROPERTIES(): 'properties' parameter must be a dictionary")
        for name, value in properties.iteritems():
            self.object().file().set_property(name=name, value=value)
            pass
        pass

    def SET_FILE_PROPERTY(self, name, value):
        if type(name) is not types.StringType:
            raise Error("SET_FILE_PROPERTY(): 'name' must be a string")
        self.object().file().set_property(name, value)
        pass
    

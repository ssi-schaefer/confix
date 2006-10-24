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

import types

from libconfix.core.machinery.builder import Builder
from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.utils.error import Error
from libconfix.core.filesys import scan

class DirectoryBuilderInterfaceProxy(InterfaceProxy):
    def __init__(self, directory_builder):
        InterfaceProxy.__init__(self)
        self.directory_builder_ = directory_builder
        self.add_global('CURRENT_BUILDER', getattr(self, 'CURRENT_BUILDER'))
        self.add_global('CURRENT_DIRECTORY', getattr(self, 'CURRENT_DIRECTORY'))
        self.add_global('ADD_DIRECTORY', getattr(self, 'ADD_DIRECTORY'))
        self.add_global('IGNORE_ENTRIES', getattr(self, 'IGNORE_ENTRIES'))
        self.add_global('IGNORE_FILE', getattr(self, 'IGNORE_FILE'))
        self.add_global('FIND_ENTRY', getattr(self, 'FIND_ENTRY'))
        self.add_global('GET_ENTRIES', getattr(self, 'GET_ENTRIES'))
        self.add_global('RESCAN_CURRENT_DIRECTORY', getattr(self, 'RESCAN_CURRENT_DIRECTORY'))
        self.add_global('ADD_EXTRA_DIST', getattr(self, 'ADD_EXTRA_DIST'))
        self.add_global('MAKEFILE_AM', getattr(self, 'MAKEFILE_AM'))
        self.add_global('ADD_BUILDER', getattr(self, 'ADD_BUILDER'))
        self.add_global('SET_FILE_PROPERTIES', getattr(self, 'SET_FILE_PROPERTIES'))
        self.add_global('SET_FILE_PROPERTY', getattr(self, 'SET_FILE_PROPERTY'))
        pass

    def CURRENT_DIRECTORY(self):
        return self.directory_builder_.directory()
    def CURRENT_BUILDER(self):
        return self.directory_builder_
    def ADD_DIRECTORY(self, name):
        return self.directory_builder_.directory().add(
            name=name,
            entry=Directory())
    def IGNORE_ENTRIES(self, names):
        if type(names) not in [types.ListType, types.TupleType]:
            raise Error('IGNORE_ENTRIES() expects a list')
        self.directory_builder_.add_ignored_entries(names)
        pass
    def IGNORE_FILE(self, name):
        # for backward compatibility with confix 1.5
        if type(name) is not types.StringType:
            raise Error('IGNORE_FILE() expects a string')
        self.directory_builder_.add_ignored_entries([name])
        pass
    def FIND_ENTRY(self, name):
        for ename, entry in self.directory_builder_.entries():
            if ename == name:
                return entry
            pass
        return None
    def GET_ENTRIES(self):
        return self.directory_builder_.entries()
    def RESCAN_CURRENT_DIRECTORY(self):
        scan.rescan_dir(self.directory_builder_.directory())
        pass
    def ADD_EXTRA_DIST(self, filename):
        self.directory_builder_.makefile_am().add_extra_dist(filename)
        pass
    def MAKEFILE_AM(self, line):
        self.directory_builder_.makefile_am().add_line(line)
        pass

    def ADD_BUILDER(self, builder):
        if not isinstance(builder, Builder):
            raise Error('ADD_BUILDER(): parameter must be a Builder')
        self.directory_builder_.add_builder(builder)
        pass

    def SET_FILE_PROPERTIES(self, filename, properties):
        if type(properties) is not types.DictionaryType:
            raise Error('SET_FILE_PROPERTIES(): properties parameter must be a dictionary')
        file = self.directory_builder_.directory().find([filename])
        if file is None:
            raise Error('SET_FILE_PROPERTIES(): '
                        'file "'+filename+'" not found in directory "'+\
                        os.sep.join(self.directory_builder_.directory().relpath())+'"')
        errors = []
        for name, value in properties.iteritems():
            try:
                file.set_property(name, value)
            except Error, e:
                errors.append(e)
                pass
            pass
        if len(errors):
            raise Error('SET_FILE_PROPERTIES('+filename+'): could not set properties', errors)
        pass

    def SET_FILE_PROPERTY(self, filename, name, value):
        file = self.directory_builder_.directory().find([filename])
        if file is None:
            raise Error('SET_FILE_PROPERTY(): '
                        'file "'+filename+'" not found in directory "'+\
                        os.sep.join(self.directory_builder_.directory().relpath())+'"')
        try:
            file.set_property(name, value)
        except Error, e:
            raise Error('SET_FILE_PROPERTY('+filename+'): could not set property "'+name+'"', [e])
        pass
        
    pass

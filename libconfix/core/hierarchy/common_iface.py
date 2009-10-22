# Copyright (C) 2007-2009 Joerg Faschingbauer

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

from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.interface import InterfaceProxy
from libconfix.core.utils.error import Error
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys import scan

import types

class DirectoryBuilderInterfaceProxy(InterfaceProxy):
    def __init__(self, dirbuilder):
        InterfaceProxy.__init__(self)

        self.__dirbuilder = dirbuilder

        self.add_global('CURRENT_BUILDER', getattr(self, 'CURRENT_BUILDER'))
        self.add_global('CWD', getattr(self, 'CWD'))
        self.add_global('CURRENT_DIRECTORY', getattr(self, 'CURRENT_DIRECTORY'))
        self.add_global('ADD_DIRECTORY', getattr(self, 'ADD_DIRECTORY'))
        self.add_global('FIND_ENTRY', getattr(self, 'FIND_ENTRY'))
        self.add_global('GET_ENTRIES', getattr(self, 'GET_ENTRIES'))
        self.add_global('RESCAN_CURRENT_DIRECTORY', getattr(self, 'RESCAN_CURRENT_DIRECTORY'))
        self.add_global('ADD_BUILDER', getattr(self, 'ADD_BUILDER'))
        self.add_global('SET_FILE_PROPERTIES', getattr(self, 'SET_FILE_PROPERTIES'))
        self.add_global('SET_FILE_PROPERTY', getattr(self, 'SET_FILE_PROPERTY'))
        pass

    def CURRENT_DIRECTORY(self):
        return self.__dirbuilder.directory()
    def CWD(self):
        return '/'.join(self.__dirbuilder.directory().relpath(self.__dirbuilder.package().rootdirectory()))
    def CURRENT_BUILDER(self):
        return self.__dirbuilder
    def ADD_DIRECTORY(self, name):
        return self.__dirbuilder.directory().add(
            name=name,
            entry=Directory())
    def FIND_ENTRY(self, name):
        for ename, entry in self.__dirbuilder.directory().entries():
            if ename == name:
                return entry
            pass
        return None
    def GET_ENTRIES(self):
        return self.__dirbuilder.directory().entries()
    def RESCAN_CURRENT_DIRECTORY(self):
        scan.rescan_dir(self.__dirbuilder.directory())
        pass

    def ADD_BUILDER(self, builder):
        if not isinstance(builder, Builder):
            raise Error('ADD_BUILDER(): parameter must be a Builder')
        self.__dirbuilder.add_builder(builder)
        pass

    def SET_FILE_PROPERTIES(self, filename, properties):
        if type(properties) is not types.DictionaryType:
            raise Error('SET_FILE_PROPERTIES(): properties parameter must be a dictionary')
        file = self.__dirbuilder.directory().find([filename])
        if file is None:
            raise Error('SET_FILE_PROPERTIES(): '
                        'file "'+filename+'" not found in directory "'+\
                        os.sep.join(self.__dirbuilder.directory().relpath())+'"')
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
        file = self.__dirbuilder.directory().find([filename])
        if file is None:
            raise Error('SET_FILE_PROPERTY(): '
                        'file "'+filename+'" not found in directory "'+\
                        os.sep.join(self.__dirbuilder.directory().relpath())+'"')
        try:
            file.set_property(name, value)
        except Error, e:
            raise Error('SET_FILE_PROPERTY('+filename+'): could not set property "'+name+'"', [e])
        pass
    pass

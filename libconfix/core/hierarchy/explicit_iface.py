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

from dirbuilder import DirectoryBuilder
from libconfix.core.machinery.interface import InterfaceProxy
from libconfix.core.utils.error import Error

class ExplicitDirectoryBuilderInterfaceProxy(InterfaceProxy):
    def __init__(self, dirbuilder):
        InterfaceProxy.__init__(self)
        self.__dirbuilder = dirbuilder
        self.add_global('DIRECTORY', getattr(self, 'DIRECTORY'))
        pass
    
    def DIRECTORY(self, path):
        if type(path) not in (list, tuple):
            raise Error('DIRECTORY('+str(path)+'): path argument must be list or tuple')
        directory = self.__dirbuilder.directory().find(path=path)
        if directory is None:
            raise Error('DIRECTORY(): could not find directory '+str(path))

        dirbuilder = DirectoryBuilder(directory=directory)
        self.__dirbuilder.add_builder(dirbuilder)
        return dirbuilder
    pass

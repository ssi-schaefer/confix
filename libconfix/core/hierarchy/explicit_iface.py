# Copyright (C) 2007 Joerg Faschingbauer

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
from confix2_dir import Confix2_dir

from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.utils.error import Error
from libconfix.core.utils import const

class ExplicitInterfaceProxy(InterfaceProxy):

    """ Implements the DIRECTORY() method of a Confix2.dir file."""
    
    def __init__(self, object):
        InterfaceProxy.__init__(self)
        self.__object = object
        self.add_global('DIRECTORY', getattr(self, 'DIRECTORY'))
        pass

    def DIRECTORY(self, path):
        directory = self.__object.parentbuilder().directory().find(path=path)
        if directory is None:
            raise Error('DIRECTORY(): could not find directory '+str(path))
        dirbuilder = DirectoryBuilder(directory=directory)
        self.__object.parentbuilder().add_builder(dirbuilder)
        confix2_dir_file = directory.get(const.CONFIX2_DIR)
        if confix2_dir_file is not None:
            dirbuilder.add_builder(Confix2_dir(file=confix2_dir_file))
            pass
        return dirbuilder

    pass

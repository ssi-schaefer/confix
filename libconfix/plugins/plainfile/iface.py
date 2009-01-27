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

import os
import types

from libconfix.core.utils.error import Error
from libconfix.core.utils import helper
from libconfix.core.machinery.builder import Builder
from libconfix.core.hierarchy.dirbuilder import DirectoryBuilder
from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.filesys.vfs_file import VFSFile

from builder import PlainFileBuilder

class ADD_PLAINFILE(InterfaceProxy):
    def __init__(self, dirbuilder):
        assert isinstance(dirbuilder, DirectoryBuilder)
        InterfaceProxy.__init__(self)
        self.__dirbuilder = dirbuilder
        self.add_global('ADD_PLAINFILE', getattr(self, 'ADD_PLAINFILE'))
        pass

    def ADD_PLAINFILE(self, filename, datadir=None, prefixdir=None):
        if type(filename) is not types.StringType:
            raise Error('ADD_PLAINFILE(): filename must be a string')
        if (datadir is not None and prefixdir is not None) or \
               (datadir is None and prefixdir is None):
            raise Error('ADD_PLAINFILE('+filename+'): specify either datadir or prefixdir')
        the_datadir = the_prefixdir = None
        if datadir is not None:
            try:
                the_datadir = helper.make_path(datadir)
            except Error, e:
                raise Error('ADD_PLAINFILE('+filename+'): datadir', [e])
            pass
        if prefixdir is not None:
            try:
                the_prefixdir = helper.make_path(prefixdir)
            except Error, e:
                raise Error('ADD_PLAINFILE('+filename+'): prefixdir', [e])
            pass

        file = self.__dirbuilder.directory().find([filename])
        if file is None:
            raise Error('ADD_PLAINFILE('+filename+'): no such file or directory')
        if not isinstance(file, VFSFile):
            raise Error('ADD_PLAINFILE('+filename+'): not a file')

        self.__dirbuilder.add_builder(
            PlainFileBuilder(file=file,
                             datadir=the_datadir,
                             prefixdir=the_prefixdir))
        pass
    pass

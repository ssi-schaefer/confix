# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2010 Joerg Faschingbauer

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

from builder import ScriptBuilder

from libconfix.core.machinery.setup import Setup
from libconfix.core.machinery.interface import InterfaceProxy
from libconfix.core.filesys.vfs_file import VFSFile
from libconfix.core.utils.error import Error

import types

class ADD_SCRIPT(InterfaceProxy):
    def __init__(self, dirbuilder):
        InterfaceProxy.__init__(self)
        self.__dirbuilder = dirbuilder
        self.add_global('SCRIPT_BIN', ScriptBuilder.BIN)
        self.add_global('SCRIPT_CHECK', ScriptBuilder.CHECK)
        self.add_global('ADD_SCRIPT', getattr(self, 'ADD_SCRIPT'))
        pass

    def ADD_SCRIPT(self, filename, what):
        if type(filename) is not types.StringType:
            raise Error('ADD_SCRIPT(): filename must be a string')
        if not what in (ScriptBuilder.BIN, ScriptBuilder.CHECK):
            raise Error('ADD_SCRIPT('+filename+', ...): "what" parameter must be one of SCRIPT_BIN and SCRIPT_CHECK') 

        file = self.__dirbuilder.directory().find([filename])
        if file is None:
            raise Error('ADD_SCRIPT('+filename+'): no such file or directory')
        if not isinstance(file, VFSFile):
            raise Error('ADD_SCRIPT('+filename+'): not a file')

        self.__dirbuilder.add_builder(ScriptBuilder(file=file, what=what))
        pass
    pass

class ScriptSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_interface(ADD_SCRIPT(dirbuilder=dirbuilder))
        pass
    pass

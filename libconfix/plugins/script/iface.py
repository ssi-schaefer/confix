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

from libconfix.core.filesys.file import File
from libconfix.core.iface.proxy import InterfaceProxy

from builder import ScriptBuilder

class ADD_SCRIPT_InterfaceProxy(InterfaceProxy):
    def __init__(self, object):
        InterfaceProxy.__init__(self)
        self.object_ = object
        self.add_global('ADD_SCRIPT', getattr(self, 'ADD_SCRIPT'))
        pass

    def ADD_SCRIPT(self, filename):
        if type(filename) is not types.StringType:
            raise Error('ADD_SCRIPT(): filename must be a string')

        file = self.object_.directory().find([filename])
        if file is None:
            raise Error('ADD_SCRIPT('+filename+'): no such file or directory')
        if not isinstance(file, File):
            raise Error('ADD_SCRIPT('+filename+'): not a file')

        self.object_.add_builder(
            ScriptBuilder(file=file,
                          parentbuilder=self.object_,
                          package=self.object_.package()))
        pass

# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2008 Joerg Faschingbauer

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

from libconfix.core.iface.executor import InterfaceExecutor
from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.machinery.filebuilder import FileBuilder
from libconfix.core.utils.error import Error

import os

class Confix2_dir(FileBuilder):
    def __init__(self, file):
        FileBuilder.__init__(self, file=file)
        self.__executed = False
        pass

    def shortname(self):
        return 'Hierarchy.Confix2_dir'

    def enlarge(self):
        super(Confix2_dir, self).enlarge()
        if self.__executed:
            return
        self.__executed = True

        ifaces = []
        # Builder.iface_pieces() is the interface that every builder
        # has, such as PROVIDE() and friends. The builders of the C
        # plugin make use of it when they parse their source files
        # (you may annotate C code with Confix instructions). A
        # directory has no such "content", but we expose its interface
        # in the directory's own Confix2.dir file.
        ifaces.extend(self.parentbuilder().iface_pieces())

        # DirectoryBuilder.interface() consists of the various
        # interfaces that the setup phase put there, for our usage.
        ifaces.extend(self.parentbuilder().interfaces())

        try:
            InterfaceExecutor(iface_pieces=ifaces).execute_file(file=self.file())
        except Error, e:
            raise Error('Could not execute file "'+\
                        os.sep.join(self.file().relpath(self.package().rootdirectory()))+'"', [e])
        pass

    pass

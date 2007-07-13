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

from confix2_dir_contributor import Confix2_dir_Contributor

from libconfix.core.iface.executor import InterfaceExecutor
from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.machinery.filebuilder import FileBuilder
from libconfix.core.utils.error import Error

import os

class Confix2_dir(FileBuilder):
    def __init__(self, file):
        FileBuilder.__init__(self, file=file)
        pass

    def shortname(self):
        return 'Hierarchy.Confix2_dir'

    def initialize(self, package):
        super(Confix2_dir, self).initialize(package)
        ifaces = self.parentbuilder().iface_pieces()[:]
        for b in self.parentbuilder().builders():
            if not isinstance(b, Confix2_dir_Contributor):
                continue
            ifaces.extend(b.get_iface_proxies())
            pass
        try:
            InterfaceExecutor(iface_pieces=ifaces).execute_file(file=self.file())
        except Error, e:
            raise Error('Could not execute file "'+\
                        os.sep.join(self.file().relpath(self.package().rootdirectory()))+'"', [e])
        pass

    def output(self):
        super(Confix2_dir, self).output()
        self.parentbuilder().makefile_am().add_extra_dist(self.file().name())
        pass

    pass

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

import os

from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.filesys import scan
from libconfix.core.utils.error import Error

class CALL_MAKE_AND_RESCAN_InterfaceProxy(InterfaceProxy):
    def __init__(self, directory_builder):
        InterfaceProxy.__init__(self)
        self.__directory_builder = directory_builder
        self.add_global('CALL_MAKE_AND_RESCAN', getattr(self, 'CALL_MAKE_AND_RESCAN'))
        pass
    def CALL_MAKE_AND_RESCAN(self, filename='Makefile', args=[]):
        args = ['make', '-f', filename] + args
        if os.spawnvp(os.P_WAIT, 'make', args) != 0:
            raise Error(
                'Error calling make in '+\
                os.sep.join(self.__directory_builder.directory().abspath()))
        scan.rescan_dir(self.__directory_builder.directory())
        pass
    pass
